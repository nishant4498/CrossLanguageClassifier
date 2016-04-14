import json
dict={}
filename='/Users/anirbanmishra/Downloads/CrossLanguageClassifier-master/ResearchProject/train_data/SampleDictionary.txt'

with open(filename,'r') as f:
    for line in f:
        word=line.split(',')
        dict[word[0]]=word[3]

with open ("dictionary.json",'a+') as fopen:
    json.dump(dict,fopen)