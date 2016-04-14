from __future__ import unicode_literals
import sys
import os
import json
import codecs
import re
from collections import defaultdict
arg1=str(sys.argv[1])
if os.path.exists('hindi_model.txt'):
    os.remove('hindi_model.txt')
wordcount={}
entertainment={}
politics={}
sports={}
business={}
hindi_stop_words=[]
hindi_model=defaultdict(dict)
punctuations = []

stop_words_path='F:/workspace/python/NLP/ResearchProject/train_data/histpwords.txt'

with open(stop_words_path,'r') as fopen:
    for line in fopen:
        line=line[0:(len(line)-1)]
        hindi_stop_words.append(line)

def printMap(tag,filename):
    if os.path.exists(filename):
        os.remove(filename)
    with codecs.open(filename,'a+','utf-8') as fopen:
        json.dump(tag,fopen)

def replace_punctuations(word):
    print word
    truncated_word = word
    for i in range (0,len(word)):
        if word[i] in punctuations:
            truncated_word =  re.sub(word[i] , "", truncated_word)
            print word[i]
    #if truncated_word =='':
    #    truncated_word = word
    return truncated_word

def populate_puntuation_list():
    with open("punctuations.txt",'r') as f:
        for line in f:
            global punctuations
            punctuations= line.decode("utf-8-sig").strip().split(" ")

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
                                flag=False
                                for stop_word in hindi_stop_words:
                                    if word.decode('utf-8')==stop_word.decode('utf-8'):
                                        #print word + stop_word
                                        flag=True
                                if(flag==False):
                                    if word.isdigit():
                                        continue
                                    else:
                                        truncated_word = replace_punctuations(word.decode("utf-8"))
                                        if(word.decode("utf-8") != truncated_word):
                                            print word.decode("utf-8") + truncated_word
                                        if truncated_word not in temp_map:
                                            temp_map[truncated_word] = 1
                                        else:
                                            temp_map[truncated_word] += 1
    return temp_map

populate_puntuation_list()
entertainment_path=os.path.join(arg1,'Entertainment/')
politics_path=os.path.join(arg1,'Politics/')
sports_path=os.path.join(arg1,'Sports/')
business_path=os.path.join(arg1,'Business/')

entertainment=build_map(entertainment_path)
politics=build_map(politics_path)
sports==build_map(sports_path)
business==build_map(business_path)

hindi_model['entertainment']=entertainment
hindi_model['politics']=politics
hindi_model['sports']=sports
hindi_model['business']=business

printMap(hindi_model,'hindi_model.txt')