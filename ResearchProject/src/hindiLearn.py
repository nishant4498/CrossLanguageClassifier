from __future__ import unicode_literals
import sys
import os
import json
import codecs
import re
from collections import defaultdict

wordcount={}
entertainment={}
politics={}
sports={}
business={}
hindi_stop_words=[]
hindi_model=defaultdict(dict)
punctuations = []
unique_words = []

train_data_path = "../train_data/hindi/"
stop_words_path='../model/stop_words.txt'

if os.path.exists('../model/hindi_model.txt'):
    os.remove('../model/hindi_model.txt')

with open(stop_words_path,'r') as fopen:
    for line in fopen:
        line=line[0:(len(line)-1)]
        hindi_stop_words.append(line)

def writeMapToFile(tag,filename):
    if os.path.exists(filename):
        os.remove(filename)
    with codecs.open(filename,'a+','utf-8') as fopen:
        json.dump(tag,fopen)

def replace_punctuations(word):
    truncated_word = word
    for i in range (0,len(word)):
        if word[i] in punctuations:
            truncated_word =  re.sub(word[i] , "", truncated_word)
    return truncated_word

def populate_puntuation_list():
    with open("../model/punctuations.txt",'r') as f:
        for line in f:
            global punctuations
            punctuations= line.decode("utf-8-sig").strip().split(" ")

def is_filter_word(words):
    for word in hindi_stop_words:
        if words == word.decode('utf-8') or words.isdigit():
            return True
    return False

def build_map(arg1):
    temp_map={}
    for root, dirs, files in os.walk(arg1):
        for file in files:
            print file
            if(file!='.DS_Store'):
                path=os.path.join(root, file)
                with open (path,'r') as fopen:
                    for line in fopen:
                        if line.decode('utf-8-sig')=='\n':
                            continue
                        else:
                            word_list=line.split()
                            for word in word_list:
                                truncated_word = replace_punctuations(word.decode("utf-8"))
                                if not is_filter_word(truncated_word):
                                    if truncated_word not in temp_map:
                                        temp_map[truncated_word] = 1
                                    else:
                                        temp_map[truncated_word] += 1
                                    if truncated_word not in unique_words:
                                        unique_words.append(truncated_word)

    return temp_map

populate_puntuation_list()
entertainment_path=os.path.join(train_data_path,'Entertainment/')
politics_path=os.path.join(train_data_path,'Politics/')
sports_path=os.path.join(train_data_path,'Sports/')
business_path=os.path.join(train_data_path,'Business/')

entertainment = build_map(entertainment_path)
politics = build_map(politics_path)
sports  = build_map(sports_path)
business = build_map(business_path)

hindi_model['entertainment']=entertainment
hindi_model['politics']=politics
hindi_model['sports']=sports
hindi_model['business']=business
hindi_model['unique_word_count'] = len(unique_words)

writeMapToFile(hindi_model,'../model/hindi_model.txt')