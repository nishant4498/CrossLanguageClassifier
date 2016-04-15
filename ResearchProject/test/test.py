from __future__ import unicode_literals
import re
import json


entertainment={}
punctuations = []
"""
with open("hindi_model.txt",'r') as f:
    model_map=json.load(f)
entertainment=model_map.get('entertainment')
for k,v in entertainment.iteritems():
    print k
    for i in range(0,len(k)):
        print k[i]
"""

with open("punctuations.txt",'r') as f:
    for line in f:
        punctuations= line.decode("utf-8-sig").strip().split(" ")

print punctuations

with open("test.txt",'r') as f:
    for line in f:
        line=line.decode('utf-8-sig')
        print line
        for word  in line.split():
            temp_word = word
            for i in range (0,len(word)):
                temp = word[i]
                if word[i] in punctuations:
                    temp_word =  re.sub(word[i] , "", temp_word)
            if temp_word=='':
                temp_word=word
            print temp_word
