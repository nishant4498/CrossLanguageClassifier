import json
classified_map={}
correct_count=0
with open("../output/Classified Marathi News.txt",'r') as fileopen:
    for line in fileopen:
        line=line.split(',')
        correct_annotation=line[1]
        predicted_annotation=line[2].strip('\n')
        if correct_annotation==predicted_annotation:
            correct_count+=1
print correct_count

