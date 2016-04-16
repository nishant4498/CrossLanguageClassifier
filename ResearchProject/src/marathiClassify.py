from __future__ import unicode_literals
from __future__ import division
import json
import re
from collections import defaultdict
import os
import math

hindi_marathi_dict = {}
entertainment = {}
politics = {}
sports = {}
business = {}
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

if os.path.exists('Classified Marathi News.txt'):
    os.remove('Classified Marathi News.txt')

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
    with open("../model/Dictionary.json",'r') as dictopen:
        global hindi_marathi_dict
        hindi_marathi_dict = json.load(dictopen)

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
    return truncated_word

def initialize_model():
    populate_hindi_model()
    poulate_dictionary()
    populate_stop_words()
    populate_punctuation_list()

initialize_model()

politics =  hindi_model.get('politics')
entertainment = hindi_model.get('entertainment')
sports = hindi_model.get('sports')
business = hindi_model.get('business')
unique_words_count = hindi_model.get('unique_word_count')

politics_keys = politics.keys()
entertainment_keys = entertainment.keys()
sports_keys = sports.keys()
business_keys = business.keys()
dictionary_keys = hindi_marathi_dict.keys()

def get_word_count(dict):
    total_word_count = 0
    for word,count in dict.iteritems():
        total_word_count += count
    return total_word_count

politics_word_totalcount = get_word_count(politics)
business_word_totalcount = get_word_count(business)
sports_word_totalcount = get_word_count(sports)
entertainment_word_totalcount = get_word_count(entertainment)

print politics_word_totalcount
print business_word_totalcount
print sports_word_totalcount
print entertainment_word_totalcount
print unique_words_count

def calculate_probability(politics_word_count,business_word_count,sports_word_count,entertainment_word_count):
    global marathi_entertainment_prob, marathi_politics_prob, marathi_business_prob, marathi_sports_prob
    print 'politics'+' '+str(politics_word_count)
    print 'business'+' '+str(business_word_count)
    print 'sports'+' '+str(sports_word_count)
    print 'entertainment'+' '+str(entertainment_word_count)

    marathi_politics_prob +=  math.log(politics_word_count/float(politics_word_totalcount + unique_words_count))
    marathi_business_prob +=  math.log(business_word_count/float(business_word_totalcount + unique_words_count))
    marathi_sports_prob +=  math.log(sports_word_count/float(sports_word_totalcount + unique_words_count))
    marathi_entertainment_prob +=  math.log(entertainment_word_count/float(entertainment_word_totalcount + unique_words_count))

    print 'politics'+' '+str(marathi_politics_prob)
    print 'business'+' '+str(marathi_business_prob)
    print 'sports'+' '+str(marathi_sports_prob)
    print 'entertainment'+' '+str(marathi_entertainment_prob)

def classify_word(truncated_word):
    print truncated_word
    if truncated_word in politics:
        politics_word_count = politics.get(truncated_word) + 1
    else:
        politics_word_count = 1
    if truncated_word in business:
        business_word_count = business.get(truncated_word) + 1
    else:
        business_word_count = 1
    if truncated_word in sports:
        sports_word_count = sports.get(truncated_word) + 1
    else:
        sports_word_count = 1
    if truncated_word in entertainment:
        entertainment_word_count = entertainment.get(truncated_word) + 1
    else:
        entertainment_word_count = 1
    calculate_probability(politics_word_count,business_word_count,sports_word_count,entertainment_word_count)

def get_hindi_word(truncated_word):
    for marathi,hindi in hindi_marathi_dict.iteritems():
        if truncated_word in marathi:
            return hindi

def get_word_index_cluster(truncated_word):
    classify_word(truncated_word)

def preprocess_word(words):
    for word in hindi_stop_words:
        if words == word.decode('utf-8') or words.isdigit():
            return True
    return False

def process_word(truncated_word):
    if truncated_word in politics or truncated_word in business or truncated_word in sports or truncated_word in entertainment:
        classify_word(truncated_word)
    else:
        get_word_index_cluster(truncated_word)

def get_news_classification():
    global marathi_entertainment_prob, marathi_politics_prob, marathi_business_prob, marathi_sports_prob
    max_probab=max(marathi_politics_prob,marathi_business_prob,marathi_sports_prob,marathi_entertainment_prob)
    if(max_probab == marathi_politics_prob):
        news_category='Politics'
    elif(max_probab == marathi_entertainment_prob):
        news_category='Entertainment'
    elif(max_probab == marathi_sports_prob):
        news_category='Sports'
    else:
        news_category='Business'
    return news_category

def create_classification_map(path,news_category):
    global news_classify
    news_classify[path]=news_category

def print_classification_map():
    global news_classify
    with open("Classified Marathi News.txt",'a+') as fileopen:
        json.dump(news_classify,fileopen)

def classify(test_data_path):
    for root, dirs, files in os.walk(test_data_path):
        for file in files:
            clear_variables()
            #print file
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
                                if not preprocess_word(truncated_word):
                                    process_word(truncated_word)
                    news_category=get_news_classification()
                    create_classification_map(path,news_category)

classify('../test_data/Business')
#classify('../test_data/Entertainment')
#classify('../test_data/Politics')
#classify('../test_data/Sports')

print_classification_map()


