from copyreg import pickle
from src.prapengolahan import Preprocessing
import pickle
import tensorflow as tf
from tensorflow.keras.preprocessing import sequence
import numpy as np



def identify_result(result):
    nilai = np.argmax(tf.matmul(result, tf.constant([1, 0, 1, 0, 0, 1, 0, 1], shape=[4, 2], dtype=tf.float32)), 1)
    if nilai[0] == 1:
       return True
    else:
        return False

def identify_text(text, fitur):
    proses = Preprocessing(text)
    token = None
    if(fitur == '0'):
        model = pickle.load(open('src/SAN_beta_2.sav', 'rb'))
        token = pickle.load(open('src/tokenizer_beta_2.pkl', 'rb'))
        clean = proses.processTweet()
    elif(fitur == '1'):
        model = pickle.load(open('src/SAN_beta_3.sav', 'rb'))
        token = pickle.load(open('src/tokenizer_beta_3.pkl', 'rb'))
        clean = proses.processTweet(stopword=False)
    elif(fitur == '2'):
        model = pickle.load(open('src/SAN_beta_4.sav', 'rb'))
        token = pickle.load(open('src/tokenizer_beta_4.pkl', 'rb'))
        clean = proses.processTweet(stemming=False)

    seq = token.texts_to_sequences(clean)
    pad = sequence.pad_sequences(seq, maxlen=len(clean[0].split()))
    predict = model.predict(pad)
    return (identify_result(predict))


