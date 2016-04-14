from __future__ import unicode_literals
import sys
import os
import json
import codecs
import re
from collections import defaultdict
#arg1=str(sys.argv[1])

hindiMarathiDict={}
entertainment={}
politics={}
sports={}
business={}
hindi_stop_words=[]
hindi_model=defaultdict(dict)
punctuations = []
unique_words_count=0

#read hindi_model.txt
with open("hindi_model.txt",'r') as fileopen:
    hindi_model=json.load(fileopen)

#read dictionary.json
with open("dictionary.json",'r') as dictopen:
    hindiMarathiDict=json.load(dictopen)

stop_words_path='/Users/anirbanmishra/Downloads/CrossLanguageClassifier-master/ResearchProject/train_data/histpwords.txt'

#build stop words list
with open(stop_words_path,'r') as fopen:
    for line in fopen:
        line=line[0:(len(line)-1)]
        hindi_stop_words.append(line)

#build puntuation list
with open("punctuations.txt",'r') as f:
    for line in f:
        punctuations= line.decode("utf-8-sig").strip().split(" ")

#removing puntuations
def replace_punctuations(word):
    truncated_word = word
    for i in range (0,len(word)):
        if word[i] in punctuations:
            truncated_word =  re.sub(word[i] , "", truncated_word)
    return truncated_word

#Reading back from hindi model
politics= hindi_model.get('politics')
entertainment=hindi_model.get('entertainment')
sports=hindi_model.get('sports')
business=hindi_model.get('business')
unique_words_count=hindi_model.get('unique_word_count')



