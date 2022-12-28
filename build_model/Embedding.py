#!/usr/bin/env python
# coding: utf-8

# In[1]:


from os.path import exists
#for data analysis and modeling
from tensorflow.keras.preprocessing import text, sequence 
import pandas as pd
import numpy as np
from collections import Counter


# In[2]:

class prepare_data:
    
    def __init__(self, fp):
        self.fp = fp
        if exists(fp):
            self.dataset = pd.read_csv(fp)
        else:
            print("Data tidak ditemukan")
        self.tokenizer = text.Tokenizer()

    def get_label(self):
        nilai_list = []
        label_list = []
        
        for index, rows in self.dataset.iterrows():
            label = [0, 0, 0, 0]
            my_list = [rows.nilai1, rows.nilai2, rows.nilai3, rows.nilai4, rows.nilai5]
            nilai_list.append(my_list) 
            #generate persebaran 4 label
            for each_key, each_value in Counter(my_list).items() :
                label[int(each_key//0.3)] = float(each_value)/5
            label_list.append(label)
            
        final_label = np.asarray(label_list, dtype='float')
        
        return final_label
    
    def load_dataset(self):
        X = self.dataset['text'].tolist()
        Y = self.get_label()
        
        n_token = []
        for i in range(len(X)):
            n_token.append(len(self.dataset['text'][i].split()))
        max_len = max(n_token)
        
        return X, Y, max_len
    
    def seq_to_pad(self, X, max_len):
        self.tokenizer.fit_on_texts(X)
        # generate the sequence of tokens
        x_seq = self.tokenizer.texts_to_sequences(X)
        # pad the sequences
        x_pad = sequence.pad_sequences(x_seq, maxlen=max_len)
        word_index = self.tokenizer.word_index

        return x_seq, x_pad, word_index

# In[3]:


class prepare_embedding:

    def __init__(self, fp, word_index):
        self.fp = fp
        self.word_index = word_index
        self.embedding_dim = 100

        
    def load_embedding(self):
        embedding_vectors = {}
        with open(self.fp,'r',encoding='utf-8') as file:
            for row in file:
                values = row.split(' ')
                word = values[0]
                weights = np.asarray([float(val) for val in values[1:]])
                embedding_vectors[word] = weights

        return embedding_vectors
    
    def embedding_matrix(self):
        embedding_vectors = self.load_embedding()
        vocab_len = len(self.word_index)+1
        embedding_matrix = np.zeros((vocab_len, self.embedding_dim))
        oov_count = 0
        oov_words = []
        for word, idx in self.word_index.items():
            if idx < vocab_len:
                embedding_vector = embedding_vectors.get(word)
                if embedding_vector is not None:
                    embedding_matrix[idx] = embedding_vector
                else:
                    oov_count += 1 
                    oov_words.append(word)

        return embedding_matrix, vocab_len