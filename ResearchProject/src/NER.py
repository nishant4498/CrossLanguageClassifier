from __future__ import unicode_literals
from __future__ import division
import json
import re
from collections import defaultdict
import os
import operator

hindi_marathi_dict = {}
entertainment_map = {}
politics_map = {}
sports_map = {}
business_map = {}
hindi_stop_words = []
hindi_model = defaultdict(dict)
punctuations  =  []
news_classify={}
unique_words_count = 0
stop_words_path = ''
politics_word_count = 0
business_word_count = 0
sports_word_count = 0
entertainment_word_count = 0
marathi_politics_prob = 0
marathi_business_prob = 0
marathi_sports_prob = 0
marathi_entertainment_prob = 0

if os.path.exists('../output/Classified_Marathi_News.txt'):
    os.remove('../output/Classified_Marathi_News.txt')

def clear_variables():
    global marathi_entertainment_prob, marathi_politics_prob, marathi_business_prob, marathi_sports_prob
    marathi_politics_prob = 0
    marathi_business_prob = 0
    marathi_sports_prob = 0
    marathi_entertainment_prob = 0
    global politics_word_count, business_word_count, sports_word_count, entertainment_word_count
    politics_word_count = 0
    business_word_count = 0
    sports_word_count = 0
    entertainment_word_count = 0

def populate_hindi_model():
    with open("../model/hindi_model.txt",'r') as fileopen:
        global hindi_model
        hindi_model = json.load(fileopen)

def poulate_dictionary():
    with open("../model/Dictionary.txt",'r') as dictopen:
        global hindi_marathi_dict
        for line in dictopen:
            words=line.split(':')
            hindi_marathi_dict[words[0]]=words[1]

def populate_stop_words():
    with open("../model/stop_words.txt",'r') as fopen:
        for line in fopen:
            line  =  line[0:(len(line)-1)]
            hindi_stop_words.append(line)

def populate_punctuation_list():
    with open("../model/punctuations.txt",'r') as f:
        for line in f:
            global punctuations
            punctuations =  line.decode("utf-8-sig").strip().split(" ")

def replace_punctuations(word):
    truncated_word  =  word
    for i in range (0,len(word)):
        if word[i] in punctuations:
            truncated_word  =   re.sub(word[i] , "", truncated_word)
        if '?' in word[i]:
            truncated_word=truncated_word.replace("?","")
        if '(' in word[i]:
            truncated_word=truncated_word.replace("(","")
        if ')' in word[i]:
            truncated_word=truncated_word.replace(")","")
        if '|' in word[i]:
            truncated_word=truncated_word.replace("|","")
    return truncated_word

def initialize_model():
    populate_hindi_model()
    poulate_dictionary()
    populate_stop_words()
    populate_punctuation_list()

initialize_model()

politics_map =  hindi_model.get('politics')
entertainment_map = hindi_model.get('entertainment')
sports_map = hindi_model.get('sports')
business_map = hindi_model.get('business')
unique_words_count = hindi_model.get('unique_word_count')

politics_words = politics_map.keys()
entertainment_words = entertainment_map.keys()
sports_words = sports_map.keys()
business_words = business_map.keys()
dictionary_words = hindi_marathi_dict.keys()


def is_filter_word(words):
    for word in hindi_stop_words:
        if words == word.decode('utf-8') or words.isdigit():
            return True
    return False


marathi_map={}


def classify(test_data_path):
    for root, dirs, files in os.walk(test_data_path):
        for file in files:
            print file
            clear_variables()
            if(file != '.DS_Store'):
                path = os.path.join(root, file)
                with open (path,'r') as fopen:
                    for line in fopen:
                        if line.decode('utf-8-sig')=='\n':
                            continue
                        else:
                            word_list = line.split()
                            for word in word_list:
                                truncated_word  =  replace_punctuations(word.decode("utf-8"))
                                if not is_filter_word(truncated_word):
                                    if truncated_word in business_words or truncated_word in entertainment_map or truncated_word in politics_words or truncated_word in sports_words:
                                        if truncated_word in marathi_map.keys():
                                            marathi_map[truncated_word]+=1
                                        else:
                                            marathi_map[truncated_word]=1

classify('../test_data/Business')
classify('../test_data/Entertainment')
classify('../test_data/Politics')
classify('../test_data/Sports')

newA = dict(sorted(marathi_map.iteritems(), key=operator.itemgetter(1), reverse=True)[:50])

for k,v in newA.iteritems():
    print k




