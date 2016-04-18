'''
Created on Apr 16, 2016

@author: dell
'''
import os
import json
from collections import defaultdict
import re
from sklearn import svm
import pickle

hindi_model = defaultdict(dict)
uniqueWordList = []
X = [] #input vector for training data (each entry in this vector is again a vector with values of parameters for that news)
Y = [] #input vector with class labels for each news

#idf = Counter

punctuations = []
punctuations_path = '../model/punctuations.txt'

hindi_stop_words=[] # hindi training so hindi stop words used
stop_words_path='../model/stop_words.txt'

unique_words_path='../model/hindi_model.txt'

def populate_stop_words():
    with open(stop_words_path,'r') as f:
        for line in f:
            line=line[0:(len(line)-1)]
            hindi_stop_words.append(line)

def replace_punctuations(word):
    truncated_word = word
    for i in range (0,len(word)):
        if word[i] in punctuations:
            truncated_word =  re.sub(word[i] , "", truncated_word)
    return truncated_word

def populate_puntuation_list():
    with open(punctuations_path,'r') as f:
        for line in f:
            global punctuations
            punctuations= line.decode("utf-8-sig").strip().split(" ")

def getUniqueWords():    
    with open(unique_words_path,'r') as fileopen:
        global hindi_model
        hindi_model = json.load(fileopen) #load hindi model from file
        global uniqueWordList
        uniqueWordList = hindi_model['unique_word_list'] # get list of unique words from model
        #uniqueWordList = sorted(uniqueWordList) # sort list

#classDirPath is directory that holds all files with classLabel
def findCount(classDirPath, classLabel):
    #print classDirPath
    global idf
    #idf = Counter(uniqueWordList) #idf is specific to class label?
    for filename in os.listdir(classDirPath): #for each file in this directory
        #print filename
        if(filename!='.DS_Store'):
            global Y
            Y.append(classLabel) #add this class label to Y vector
            
            with open(classDirPath+'/'+filename,'r') as f:
                
                wordVector = {}#Counter(uniqueWordList) # all values are initialized to 1
                #wordVector = [0] * len(uniqueWordList)
                
                #flagList = [0] * len(uniqueWordList) #to be used for idf values
                
                for line in f:            
                    if line.decode('utf-8-sig')=='\n': #if empty line
                        continue
                    else:
                        word_list=line.split() #obtain each word in the line                
                        for word in word_list:
                            flag=False  
                            # use utf-8 or utf-8-sig?
                                                  
                            truncated_word = replace_punctuations(word.decode("utf-8")) # replace punctuations in the word
                            #print truncated_word
                            
                            # remove stop words/ do not consider for further processing
                            for stop_word in hindi_stop_words:
                                if truncated_word == stop_word.decode('utf-8'):
                                    #print 'truncated_word is stop word'
                                    flag=True
                                    break
                            
                            if(flag==False): #if not a stop word
                                #print truncated_word+'dup'
                                if truncated_word.isdigit():
                                    #print 'isDigit'
                                    continue
                                else:
                                    #print 'update count of word'
                                    if(truncated_word in uniqueWordList): #why to check this condition?
                                        #print 'word present in uniqueList',uniqueWordList.index(truncated_word)
                                        #wordVector[truncated_word] += 1 #increment counter by 1
                                        # indices are analogous
                                        if not wordVector.has_key(truncated_word):
                                            wordVector[truncated_word]=1
                                        else:
                                            wordVector[truncated_word]=wordVector[truncated_word]+1 
                                        
                                        '''
                                        if flagList[uniqueWordList.index(truncated_word)] != 0: # use this word only once
                                            print 'add 1 to idf',flagList[uniqueWordList.index(truncated_word)]
                                            #global idf
                                            idf[truncated_word] += 1 # this word is found in this document
                                            flagList[uniqueWordList.index(truncated_word)] = 1
                                        '''
                                    #else:
                                        #print 'Word not in unique word list'
                #print wordVector    
                #sorted(wordVector)   
                for remaining in uniqueWordList:
                    if not wordVector.has_key(remaining):
                        wordVector[remaining]=0    
                        
                wordArray=[]    
                for word in sorted(wordVector.keys()):
                    wordArray.append(wordVector[word])
                '''
                wordVectorArray = []
                for key in uniqueWordList:
                    #print key                    
                    print wordVector[key.decode("utf-8-sig")]
                    wordVectorArray.append(wordVector[key])
                print len(wordVectorArray)
                
                wordVectorArray = wordVector.values()
                wordVectorArray[:] = [x - 1 for x in wordVectorArray]
                '''

                global X 
                X.append(wordArray)
                #X.append(wordVectorArray) # add wordVector for this news in X
                #print len(X)
    
def multiplyIDFValues():
    print "Implement idf function"            
# unique word list is sorted
# wordVector contains tf-idf value of that corresponding index word

getUniqueWords()
print uniqueWordList
print len(uniqueWordList)
#print uniqueWordList

train_data_path = "../train_data/hindi/"
entertainment_path=os.path.join(train_data_path,'Entertainment/')
politics_path=os.path.join(train_data_path,'Politics/')
sports_path=os.path.join(train_data_path,'Sports/')
business_path=os.path.join(train_data_path,'Business/')

findCount(entertainment_path,"Entertainment")
# multiply all vectors with all idf values for this class
findCount(politics_path,"Politics")
findCount(sports_path,"Sports")
findCount(business_path,"Business")

# learn svm model
lin_clf = svm.LinearSVC()
lin_clf.fit(X, Y) 
print lin_clf

with open('../model/svmmodel.txt', 'w') as f:
    pickle.dump(lin_clf,f)
print "svm model generated and written to file"

'''
print 'X input vector'
for x in range(0,10):
    print X[x] 


#test class label using svm model
test = X # 100% accuracy!
#test.append(X[1])
#print test
print lin_clf.predict(test)
print Y
''' 