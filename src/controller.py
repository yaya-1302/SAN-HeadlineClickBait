from copyreg import pickle
from src.prapengolahan import Preprocessing
import pickle
import tensorflow as tf
from tensorflow.keras.preprocessing import sequence
import numpy as np
import re


def identify_result(result):
    nilai = np.argmax(tf.matmul(result, tf.constant([1, 0, 1, 0, 0, 1, 0, 1], shape=[4, 2], dtype=tf.float32)), 1)
    if nilai[0] == 1:
       return True
    else:
        return False

def identify_text(text):
    proses = Preprocessing(text)
    model = pickle.load(open('src/SAN_beta_2.sav', 'rb'))
    token = pickle.load(open('src/tokenizer_beta_2.pkl', 'rb'))
    clean = proses.processTweet()
    seq = token.texts_to_sequences(clean)
    pad = sequence.pad_sequences(seq, maxlen=len(clean[0].split()))
    predict = model.predict(pad)
    return (identify_result(predict))

def clean(text):
    cleaned = text.lower()
    # removing retweet and mention
    cleaned = re.sub(r"(?:r?t?|v?i?a) ?@[a-z0-9_]+", "", cleaned)
    # removing hastag
    cleaned = re.sub(r"#[a-z0-9_]+", "", cleaned)
    # removing hyperlinks in the tweet
    cleaned = re.sub(r" ?https:\/\/t\.co\/[-a-zA-Z0-9@:%._\+~#=]{1,256}", "", cleaned)
    return cleaned.title()

