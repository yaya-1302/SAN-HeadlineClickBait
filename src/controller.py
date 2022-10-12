
from src.prapengolahan import Preprocessing
import pickle
import tensorflow as tf
from tensorflow.keras.preprocessing import sequence
import numpy as np
import re
from tensorflow import keras
from tensorflow.keras import layers

class self_attention(layers.Layer):
    def __init__(self,**kwargs):
        super(self_attention,self).__init__(**kwargs)
        
    def build(self, input_shape):
        self.w = self.add_weight(name = 'attention_weight',
                                 shape = (input_shape[-1], input_shape[-1]),
                                 initializer = 'GlorotNormal',
                                 trainable = True)
        
        self.b = self.add_weight(name = 'attention_bias',
                                 shape = (input_shape[-1], 1),
                                 initializer = 'GlorotNormal',
                                 trainable = True)
        super(self_attention, self).build(input_shape)
        
    def call(self, input):
        step1 = tf.math.tanh(tf.matmul(input, self.w))
        step2 = tf.squeeze(tf.matmul(step1, self.b), axis=-1)
        alpha = tf.keras.activations.softmax(step2)
        att = tf.expand_dims(alpha, axis=-1)
        output = input*att
        return tf.keras.backend.sum(output, axis=1)
    
    def get_config(self):
        config = super(self_attention,self).get_config()
        return config

def custom_loss(y_true, y_pred):
  mean_y_actual = tf.matmul(y_true, tf.constant([0, 0.3333333333, 0.6666666666, 1.0], shape=[4, 1]))
  mean_y_pred = tf.matmul(y_pred, tf.constant([0, 0.3333333333, 0.6666666666, 1.0], shape=[4, 1]))
  mse = tf.keras.losses.MeanSquaredError()
  return mse(mean_y_actual, mean_y_pred)

def custom_accuracy(y_true, y_pred):
  actual = tf.argmax(tf.matmul(y_true, tf.constant([1, 0, 1, 0, 0, 1, 0, 1], shape=[4, 2], dtype=tf.float32)),1 )
  pred = tf.argmax(tf.matmul(y_pred, tf.constant([1, 0, 1, 0, 0, 1, 0, 1], shape=[4, 2], dtype=tf.float32)), 1)
  correct = 0
  for i in range(len(actual)):
    if actual[i] == pred[i]:
      correct += 1
  acc = float(correct)/float(len(actual))
  return acc

def identify_result(result):
    val = tf.matmul(result, tf.constant([1, 0, 1, 0, 0, 1, 0, 1], shape=[4, 2], dtype=tf.float32))
    nilai = np.argmax(val, 1)
    if nilai[0] == 1:
       return True, str(val.numpy()[0][1])
    else:
        return False, str(val.numpy()[0][0])

def identify_text(text):
    proses = Preprocessing(text)
    model = tf.keras.models.load_model('src/model_10epoch_fold_4.h5', 
                                          custom_objects = {
                                              "self_attention": self_attention,
                                              "custom_loss": custom_loss,
                                              "custom_accuracy": custom_accuracy
                                          })
    token = pickle.load(open('src/tokenizer_final.pkl', 'rb'))
    clean = proses.processTweet()
    seq = token.texts_to_sequences(clean)
    pad = sequence.pad_sequences(seq, maxlen=len(clean[0].split()))
    predict = model.predict(pad)
    result, value = identify_result(predict)
    return result, value

def clean(text):
    cleaned = text.lower()
    # removing retweet and mention
    cleaned = re.sub(r"(?:r?t?|v?i?a) ?@[a-z0-9_]+", "", cleaned)
    # removing hastag
    cleaned = re.sub(r"#[a-z0-9_]+", "", cleaned)
    # removing hyperlinks in the tweet
    cleaned = re.sub(r" ?https:\/\/t\.co\/[-a-zA-Z0-9@:%._\+~#=]{1,256}", "", cleaned)
    return cleaned.title()

def text_length(text):
    return len(text.split()), len(text)