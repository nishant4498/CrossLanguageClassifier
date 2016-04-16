'''
Created on Apr 13, 2016

@author: dell
'''

from sklearn.metrics import f1_score

'''
y_true = [0, 1, 2, 0, 1, 2]
y_pred = [0, 2, 1, 0, 0, 1]
print f1_score(y_true, y_pred, average='macro')  
print f1_score(y_true, y_pred, average='micro')  
print f1_score(y_true, y_pred, average='weighted')  
print f1_score(y_true, y_pred, average=None)

'''

rootPath = "G:\USC\Spring2016\NLP\NLPProject\SampleResult.txt"
#rootPath = "G:/USC/Spring2016/NLP/Workspace/NaiveBayesClassifier/nboutput.txt"

y_true = []
y_pred = []

with open(rootPath,'r') as f:    
    for line in f:         
        #print line   
        line = line.replace("\n", "")              
        classes = line.split(",")  #comma separated line with filePath, annotated class and classified class
        #print classes
        y_true.append(classes[1])
        y_pred.append(classes[2])
        
#print y_true
#print y_pred

#label = [""]

#what does micro, macro, weighted signify?
print f1_score(y_true, y_pred, average='macro')  
print f1_score(y_true, y_pred, average='micro')  
print f1_score(y_true, y_pred, average='weighted')  
print f1_score(y_true, y_pred, average=None) 

'''
average : string, [None, ‘binary’ (default), ‘micro’, ‘macro’, ‘samples’, ‘weighted’]
This parameter is required for multiclass/multilabel targets. If None, the scores for each class are returned. Otherwise, this determines the type of averaging performed on the data:
'binary':
Only report results for the class specified by pos_label. This is applicable only if targets (y_{true,pred}) are binary.
'micro':
Calculate metrics globally by counting the total true positives, false negatives and false positives.
'macro':
Calculate metrics for each label, and find their unweighted mean. This does not take label imbalance into account.
'weighted':
Calculate metrics for each label, and find their average, weighted by support (the number of true instances for each label). This alters ‘macro’ to account for label imbalance; it can result in an F-score that is not between precision and recall.
'samples':
Calculate metrics for each instance, and find their average (only meaningful for multilabel classification where this differs from accuracy_score).
Note that if pos_label is given in binary classification with average != ‘binary’, only that positive class is reported. This behavior is deprecated and will change in version 0.18.
'''