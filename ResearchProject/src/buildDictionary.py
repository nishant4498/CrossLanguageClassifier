import json
dict={}
dictionary_text_file = '../model/MarathiHindiDictionary.txt'

with open(dictionary_text_file,'r') as f:
    for line in f:
        word=line.split(',')
        dict[word[0]]=word[3]

with open ("../model/Dictionary.json",'a+') as fopen:
    json.dump(dict,fopen)