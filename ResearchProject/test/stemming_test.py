
def check_for_cluster(word):
    if(len(word) > 5):
        return True
    else:
        return False

def generate_word_cluster(word):
    word_cluster = []
    start_index = get_start_index_for_cluster(word)
    end_index = len(word)
    print "word= " + word + " len=" + str(len(word))
    for i in range(start_index ,end_index):
        print word[0:i]
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



with open("test.txt",'r') as f:
    for line in f:
     if line.decode('utf-8-sig')=='\n':
        continue
    else:
        word_list=line.split()
        for word in word_list:
            word = word.decode('utf-8-sig')
            if(check_for_cluster(word)):
                word_cluster = generate_word_cluster(word)
            else:
                print "No cluster for this:" + word

