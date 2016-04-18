from __future__ import unicode_literals
from __future__ import division
import json
import re
from collections import defaultdict
import os
import math

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

if os.path.exists('../output/Classified Marathi News.txt'):
    os.remove('../output/Classified Marathi News.txt')

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

def get_word_count(dict):
    total_word_count = 0
    for word,count in dict.iteritems():
        total_word_count += count
    return total_word_count

politics_word_totalcount = get_word_count(politics_map)
business_word_totalcount = get_word_count(business_map)
sports_word_totalcount = get_word_count(sports_map)
entertainment_word_totalcount = get_word_count(entertainment_map)

def check_for_cluster(word):
    if(len(word) > 5):
        return True
    else:
        return False

def generate_word_cluster(word):
    word_cluster = []
    start_index = get_start_index_for_cluster(word)
    end_index = len(word)
    #print "word= " + word + " len=" + str(len(word))
    for i in range(start_index ,end_index):
        #print word[0:i]
        word_cluster.append(word[0:i])
    return word_cluster

def get_start_index_for_cluster(word):
    word_length = len(word)
    if 5 <= word_length  <= 7:
        return word_length - 2
    elif 7 <= word_length  <= 10:
        return word_length - 4
    else:
        return word_length - 7

def calculate_news_file_probability(politics_word_count,business_word_count,sports_word_count,entertainment_word_count):
    global marathi_entertainment_prob, marathi_politics_prob, marathi_business_prob, marathi_sports_prob
    """print 'politics'+' '+str(politics_word_count)
    print 'business'+' '+str(business_word_count)
    print 'sports'+' '+str(sports_word_count)
    print 'entertainment'+' '+str(entertainment_word_count)"""

    marathi_politics_prob +=  math.log(politics_word_count/float(politics_word_totalcount + unique_words_count))
    marathi_business_prob +=  math.log(business_word_count/float(business_word_totalcount + unique_words_count))
    marathi_sports_prob +=  math.log(sports_word_count/float(sports_word_totalcount + unique_words_count))
    marathi_entertainment_prob +=  math.log(entertainment_word_count/float(entertainment_word_totalcount + unique_words_count))

    """print 'politics'+' '+str(marathi_politics_prob)
    print 'business'+' '+str(marathi_business_prob)
    print 'sports'+' '+str(marathi_sports_prob)
    print 'entertainment'+' '+str(marathi_entertainment_prob)"""

def compute_word_category_probability(truncated_word):
    if truncated_word in politics_words:
        politics_word_count = politics_map.get(truncated_word) + 1
    else:
        politics_word_count = 1
    if truncated_word in business_words:
        business_word_count = business_map.get(truncated_word) + 1
    else:
        business_word_count = 1
    if truncated_word in sports_words:
        sports_word_count = sports_map.get(truncated_word) + 1
    else:
        sports_word_count = 1
    if truncated_word in entertainment_words:
        entertainment_word_count = entertainment_map.get(truncated_word) + 1
    else:
        entertainment_word_count = 1
    calculate_news_file_probability(politics_word_count,business_word_count,sports_word_count,entertainment_word_count)

def get_hindi_translation(truncated_word):
    for marathi,hindi in hindi_marathi_dict.iteritems():
        if truncated_word in marathi:
            return hindi

def is_filter_word(words):
    for word in hindi_stop_words:
        if words == word.decode('utf-8') or words.isdigit():
            return True
    return False

def apply_classification_algorithm(truncated_word):
    if truncated_word in politics_words or truncated_word in business_words or truncated_word in sports_words or truncated_word in entertainment_words:
        compute_word_category_probability(truncated_word)
    elif truncated_word in dictionary_words:
        hindi_word = get_hindi_translation(truncated_word)
        if '/' in hindi_word:
            hindi_word_list=hindi_word.split('/')
            for word in hindi_word_list:
                if word in politics_words or word in business_words or word in sports_words or word in entertainment_words:
                    compute_word_category_probability(word)
                    break
        else:
            compute_word_category_probability(hindi_word)
    elif(check_for_cluster(truncated_word)):
        word_cluster = generate_word_cluster(truncated_word)
        for i in range(len(word_cluster)-1,0,-1):
            if word_cluster[i] in politics_words or word_cluster[i] in business_words or word_cluster[i] in sports_words or word_cluster[i] in entertainment_words:
                compute_word_category_probability(word_cluster[i])
                break
    else:
        compute_word_category_probability(truncated_word)

def classify_news_file():
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

def create_output_map(path,news_category):
    global news_classify
    news_classify[path]=news_category

def write_output_to_file():
    global news_classify
    with open("../output/Classified Marathi News.txt",'a+') as fileopen:
        for path, classification in news_classify.iteritems():
            fileopen.write(path+','+path.split('/')[2].split('\\')[0]+','+classification+'\n')

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
                                    apply_classification_algorithm(truncated_word)
                    news_category=classify_news_file()
                    create_output_map(path,news_category)

classify('../test_data/Business')
classify('../test_data/Entertainment')
classify('../test_data/Politics')
classify('../test_data/Sports')

write_output_to_file()


