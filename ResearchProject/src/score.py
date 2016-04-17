import json
classified_map={}
with open("../output/Classified Marathi News.txt",'r') as fileopen:
    classified_map=json.load(fileopen)

correct_count=0

for file,classification in classified_map.iteritems():
    if 'Politics' in file and 'Politics' in classification:
        correct_count+=1
    elif 'Sports' in file and 'Sports' in classification:
        correct_count+=1
    elif 'Entertainment' in file and 'Entertainment' in classification:
        correct_count+=1
    elif 'Business' in file and 'Business' in classification:
        correct_count+=1

print correct_count

