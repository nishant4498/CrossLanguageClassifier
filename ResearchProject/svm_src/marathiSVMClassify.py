
import os
import json
import re
import pickle

uniqueWordList=[]
punctuations  =  []
ultimateTestArray={}
ourDictionary={}  

unique_words_path='../model/hindi_model.txt'
punctuations_path = '../model/punctuations.txt'
dictionary_path = '../model/Dictionary.json'

def populate_punctuation_list():
    with open(punctuations_path,'r') as f:
        for line in f:
            punctuations =  line.decode("utf-8-sig").strip().split(" ")
    return punctuations 

def replace_punctuations(word):
    truncated_word  =  word
    for i in range (0,len(word)):
        if word[i] in punctuations:
            truncated_word  =   re.sub(word[i] , "", truncated_word)
    return truncated_word

'''
def is_filter_word(words):
    for word in hindi_stop_words:
        if words == word.decode('utf-8') or words.isdigit():
            return True
    return False   
''' 
 
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

def getUniqueWords():    
    with open(unique_words_path,'r') as fileopen:
        hindi_model = json.load(fileopen)
        uniqueWordList = hindi_model['unique_word_list']
        return uniqueWordList

#Execution of code

uniqueWordList=getUniqueWords()

punctuations=populate_punctuation_list()

with open(dictionary_path,'r') as f: 
    hindi_marathi_dict=json.load(f)

for key,value in hindi_marathi_dict.iteritems():
    for c in key:
        if '"' in c:
            key=key.replace('"','')
    for c in value:
        if '"' in c:
            value=value.replace('"','')        
    ourDictionary[key]=value
    
 
# path  
def classify(path):    
    for root, dirs, files in os.walk(path):
            for f1 in files:
                #print f1+"\n"
                if f1.endswith(".txt"):
                    filee = os.path.join(root, f1)
                    with open(filee, 'r') as my_file:
                        vectorOffile={}                
                        fileContent = my_file.readlines()
                        for line in fileContent:
                            line=line.decode('utf-8-sig')
                            if line =='\n':
                                continue
                            else :
                                wordArray=line.split()
                                for word in wordArray:
                                    word  =  replace_punctuations(word)
                                    #print "checking word //"+word+"///" 
                                        
                                    if word in uniqueWordList:
                                        #print word+" in uniquewordlist" 
                                        if not vectorOffile.has_key(word):
                                            vectorOffile[word]=1
                                        else:    
                                            vectorOffile[word]=vectorOffile[word]+1
                                    elif  ourDictionary.has_key(word):
                                        #print word+" in disctionary"
                                        meanings=ourDictionary[word]
                                        meaningarray=meanings.split("/")
                                        
                                        for m in meaningarray:        
                                            if m in uniqueWordList:
                                                #print "   "+m+" unique in d"
                                                if not vectorOffile.has_key(m):
                                                    vectorOffile[m]=1
                                                else:
                                                    vectorOffile[m]=vectorOffile[m]+1    
                                    elif  check_for_cluster(word) == True:
                                        wordcluster = generate_word_cluster(word)
                                        for w in wordcluster:
                                            if w in uniqueWordList:
                                                #print w+" stemmed in uniquewordlist"
                                                if not vectorOffile.has_key(w):
                                                    vectorOffile[w]=1
                                                else:    
                                                    vectorOffile[w]=vectorOffile[w]+1
                                                break    
                                            elif  ourDictionary.has_key(w):
                                                #print "**"+w+" stemmed in dictionary"
                                                meanings=ourDictionary[w]
                                                meaningarray=meanings.split("/")
                                        
                                                for m in meaningarray:        
                                                    if m in uniqueWordList:
                                                        #print "  stemmed  "+m+" unique in d"
                                                        if not vectorOffile.has_key(m):
                                                            vectorOffile[m]=1
                                                        else:
                                                            vectorOffile[m]=vectorOffile[m]+1 
                                                break  
                                    #else:
                                        #print word+" not found"
                                    
                        
                        for remaining in uniqueWordList:
                            if not vectorOffile.has_key(remaining):
                                vectorOffile[remaining]=0
                             
                        arrayOfFile=[]    
                        for word in sorted(vectorOffile.keys()):
                            arrayOfFile.append(vectorOffile[word])
                        
                        ultimateTestArray[filee]=arrayOfFile  
print "Read test data"
finalArray=[] #contains test data vectors
fileArray = [] #contains list of test files in order as read 
classArray = [] #contains list of class labels of test files in order as read

#Read business test data files
classify('../test_data/Business')                           
for f in sorted(ultimateTestArray.keys()):
    fileArray.append(f)
    classArray.append("Business")
    finalArray.append(ultimateTestArray[f])
print "Business read"
#print finalArray
#print len(finalArray)

ultimateTestArray={}
classify('../test_data/Entertainment')
for f in sorted(ultimateTestArray.keys()):
    fileArray.append(f)
    classArray.append("Entertainment")
    finalArray.append(ultimateTestArray[f])
print "Entertainment read"
#print finalArray
#print len(finalArray)
ultimateTestArray={}
classify('../test_data/Politics')
for f in sorted(ultimateTestArray.keys()):
    fileArray.append(f)
    classArray.append("Politics")
    finalArray.append(ultimateTestArray[f])
print "Politics read"
#print finalArray
#print len(finalArray)
ultimateTestArray={}
classify('../test_data/Sports')
for f in sorted(ultimateTestArray.keys()):
    fileArray.append(f)
    classArray.append("Sports")
    finalArray.append(ultimateTestArray[f])
print "Sports read"

'''
def write_output_to_file():
    global news_classify
    with open("Classified Marathi News.txt",'a+') as fileopen:
        json.dump(news_classify,fileopen)
write_output_to_file() 
for f in sorted(ultimateTestArray.keys()):
    print f
for u in finalArray:
    print len(u)                                 
'''
    
print "Svm model read from file"                                
with open('../model/svmmodel.txt', 'r') as f:
    lin_clf = pickle.load(f)

print "Predict result"
result = lin_clf.predict(finalArray)

op_file = open("../output/Classified_Marathi_News_SVM.txt", "w")

print "Write svm classification output to file"
for x in range(0,len(fileArray)):
    print fileArray[x],",",classArray[x],",",result[x]   
    op_file.write(fileArray[x]+","+classArray[x]+","+result[x]+"\n")