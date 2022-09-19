#!/usr/bin/env python
# coding: utf-8

# In[12]:


import time
from os.path import exists
import pandas as pd
from collections import Counter 
import re
import numpy as np
import string
from num2words import num2words
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

class Preprocessing:
    
    def __init__(self, data):
        
        if data[-4:] == ".csv":
            if exists(data):
                self.dataset = pd.read_csv(data)
                self.data = self.dataset['text'].tolist()
            else:
                print("file data tidak ditemukan")
        else:
            self.data = data
               
        self.stopwords = pd.read_csv('/home/asus/Desktop/clickbait/src/stopwords.csv')['Kata'].tolist()
        
    def numtoword(self, data):
        dataList = data.split()
        for i in range(len(dataList)):
            if dataList[i].isnumeric():
                dataList[i] = num2words(int(dataList[i]), lang='id')
        result = ' '.join(dataList)
        # untuk menghapus angka yang tidak dapat di konversi, seperti float ataupun currency
        finalresult = ''.join([i for i in result if not i.isdigit()])
        
        return finalresult
    
    def stopword_removal(self, data):
        cleaned = ' '.join([word for word in data.split() if word not in (self.stopwords)])
        return cleaned
        
    def stemmer(self, data):
        factory = StemmerFactory()
        stemmer = factory.create_stemmer()
        result = stemmer.stem(data)
        return result
 
    def processTweet(self,  stemming=True, stopword=True):
        cleanedList = []
        if type(self.data) is list:
            for data in self.data:
                try:
                    cleantweet = data.lower()
                    # removing retweet and mention
                    cleantweet = re.sub(r"(?:r?t?|v?i?a) ?@[a-z0-9_]+", "", cleantweet)
                    # removing hastag
                    cleantweet = re.sub(r"#[a-z0-9_]+", "", cleantweet)
                    # removing hyperlinks in the tweet
                    cleantweet = re.sub(r" ?https:\/\/t\.co\/[-a-zA-Z0-9@:%._\+~#=]{1,256}", "", cleantweet)
                    #remove special character
                    cleantweet = re.sub(r"[^a-z0-9 ]", "", cleantweet)
                    cleantweet.strip()
                    #stemming
                    if stemming != True:
                        pass
                    else:
                        cleantweet = self.stemmer(cleantweet)
                    #stopword removal
                    if stopword != True:
                        pass
                    else:
                        cleantweet = self.stopword_removal(cleantweet)
                    #number to word
                    cleantweet = self.numtoword(cleantweet)
                
                    cleanedList.append(cleantweet)
                
                except BaseException as e:
                    print('failed on_status,',str(e))
                    time.sleep(3)
        else:
            cleantweet = self.data.lower()
            # removing retweet and mention
            cleantweet = re.sub(r"(?:r?t?|v?i?a) ?@[a-z0-9_]+", "", cleantweet)
            # removing hastag
            cleantweet = re.sub(r"#[a-z0-9_]+", "", cleantweet)
            # removing hyperlinks in the tweet
            cleantweet = re.sub(r" ?https:\/\/t\.co\/[-a-zA-Z0-9@:%._\+~#=]{1,256}", "", cleantweet)
            #remove special character
            cleantweet = re.sub(r"[^a-z0-9 ]", "", cleantweet)
            cleantweet.strip()
            #stemming
            if stemming != True:
                pass
            else:
                cleantweet = self.stemmer(cleantweet)
            #stopword removal
            if stopword != True:
                pass
            else:
                cleantweet = self.stopword_removal(cleantweet)
            #number to word
            cleantweet = self.numtoword(cleantweet)
                
            cleanedList.append(cleantweet)
        return cleanedList
    
    def savepreprocess(self, cleanlist, namaFile):

        print('memulai proses penyimpanan')
        for i in range (len(self.data)):
            self.dataset['text'] = self.dataset['text'].replace(self.data[i], cleanlist[i])
    
        self.dataset.loc[self.dataset["Label"] == "Clickbait", "Label"] = 1
        self.dataset.loc[self.dataset["Label"] == "Non-Clickbait", "Label"] = 0
        
        newFile = self.dataset.to_csv(namaFile, index=False)
        print("Dataset hasil Preprocessing telah tersimpan")
        return namaFile

