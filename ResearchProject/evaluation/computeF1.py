'''
Created on Apr 13, 2016

@author: dell
'''

from sklearn.metrics import f1_score

def calculateScore(path):
    y_true = []
    y_pred = []
    
    with open(path,'r') as f:    
        for line in f:         
            #print line   
            line = line.replace("\n", "")              
            classes = line.split(",")  #comma separated line with filePath, annotated class and classified class
            #print classes
            y_true.append(classes[1])
            y_pred.append(classes[2])
            
    #what does micro, macro, weighted signify?     
    print "Calculate metrics globally by counting the total true positives, false negatives and false positives\nF1 score="
    print f1_score(y_true, y_pred, average='micro') 
    '''
    print "average='macro'"
    print f1_score(y_true, y_pred, average='macro') 
    print "average='weighted'" 
    print f1_score(y_true, y_pred, average='weighted')  
    print "average=None"
    print f1_score(y_true, y_pred, average=None)
    '''

filePath = "../output/Classified_Marathi_News_NB.txt"
print "F1 score for Naive Bayes classification"
calculateScore(filePath)
filePath = "../output/Classified_Marathi_News_SVM.txt"
print "F1 score for SVM classification"
calculateScore(filePath)