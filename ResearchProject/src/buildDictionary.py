import json
import re
dict={}
dictionary_text_file = '../model/MarathiHindiDictionary.txt'

punctuations=[]
puntuation_list=[]

def populate_puntuation_list():
    with open("../model/punctuations.txt",'r') as f:
        for line in f:
            puntuation_list=line.split()
            for puntuation in puntuation_list:
                global punctuations
                punctuations= puntuation.decode("utf-8").strip().split(" ")

def replace_punctuations(word):
    truncated_word = word
    for i in range (0,len(word)):
        if word[i] in punctuations:
            truncated_word = re.sub(word[i] , "", truncated_word)
    return truncated_word

with open(dictionary_text_file,'r') as f:
    populate_puntuation_list()
    for line in f:
        word=line.split(',')
        truncated_marathi_word=replace_punctuations(word[0].decode('utf-8'))
        truncated_hindi_word=replace_punctuations(word[3].decode('utf-8'))
        dict[truncated_marathi_word]=truncated_hindi_word

with open ("../model/Dictionary.txt",'a+') as fopen:
    json.dump(dict,fopen)