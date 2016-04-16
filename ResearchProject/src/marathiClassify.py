from __future__ import unicode_literals
import json
import re
from collections import defaultdict

hindi_marathi_dict={}
entertainment={}
politics={}
sports={}
business={}
hindi_stop_words=[]
hindi_model=defaultdict(dict)
punctuations = []
unique_words_count=0

stop_words_path=''

def populate_hindi_model():
    with open("../model/hindi_model.txt",'r') as fileopen:
        global hindi_model
        hindi_model=json.load(fileopen)

def poulate_dictionary():
    with open("../model/Dictionary.json",'r') as dictopen:
        global hindi_marathi_dict
        hindi_marathi_dict=json.load(dictopen)

def populate_stop_words():
    with open("../model/stop_words.txt",'r') as fopen:
        for line in fopen:
            line = line[0:(len(line)-1)]
            hindi_stop_words.append(line)

def populate_punctuation_list():
    with open("../model/punctuations.txt",'r') as f:
        for line in f:
            global punctuations
            punctuations= line.decode("utf-8-sig").strip().split(" ")


def replace_punctuations(word):
    truncated_word = word
    for i in range (0,len(word)):
        if word[i] in punctuations:
            truncated_word =  re.sub(word[i] , "", truncated_word)
    return truncated_word

def initialize_model():
    populate_hindi_model()
    poulate_dictionary()
    populate_stop_words()
    populate_punctuation_list()

initialize_model()


politics= hindi_model.get('politics')
entertainment=hindi_model.get('entertainment')
sports=hindi_model.get('sports')
business=hindi_model.get('business')
unique_words_count=hindi_model.get('unique_word_count')

print politics
print entertainment
print sports
print business
print unique_words_count



