#NLP Assignment 1 - Niranjana Kandavel - 21st September 2016
import os
import pickle
from collections import defaultdict
import sys

#get input file path
#file_path = '/home/ninja/PycharmProjects/NlpAssign1/tenpercent_ravi'
file_path = '/home/ninja/PycharmProjects/NlpAssign1/spamham/train'
#file_path = sys.argv[1]

#defining dictionary for all words, spam words, ham words and count of ham files, spam files
all_word_count = defaultdict(int)
spam_word_count = defaultdict(int)
ham_word_count = defaultdict(int)
file_count = defaultdict(int)

#defining and initializing variables for counting
spam_file_count = 0
ham_file_count = 0
spam_all_words = 0
ham_all_words = 0
all_words = 0


#recursively going through each file and calculate all the counts
for root, dirs, files in os.walk(file_path):
    for file in files:
        fullfilename = os.path.join(root, file)
        if file.endswith('spam.txt'):
            spam_file_count += 1
            for w in open(fullfilename, "r", encoding="latin1").read().split():
                all_word_count[w] += 1
                spam_word_count[w] += 1
                spam_all_words += 1
                all_words += 1
        elif file.endswith('ham.txt'):
            ham_file_count += 1
            for w in open(fullfilename, "r", encoding="latin1").read().split():
                all_word_count[w] += 1
                ham_word_count[w] += 1
                ham_all_words += 1
                all_words += 1

#updating file counts, non-duplicate word counts into the dictionary
file_count["spam"] = spam_file_count/(spam_file_count+ham_file_count)
file_count["ham"] = ham_file_count/(spam_file_count+ham_file_count)
file_count["spamwords"] = spam_all_words
file_count["hamwords"] = ham_all_words
file_count["all_words"] = all_words

#building the nested dictionary
words_count = defaultdict(dict)
words_count["spam"] = spam_word_count
words_count["ham"] = ham_word_count
words_count["all"] = all_word_count
words_count["file"] = file_count

#building the nbmodel.txt using pickle
pickle.dump(words_count, open("nbmodel.txt","wb"))

#to be commented
print ('Spam words with duplicates : '+str(spam_all_words))
print ('Ham words with duplicates : '+str(ham_all_words))
print ('complete total spam file : '+str(spam_file_count))
print ('complete total ham file : '+str(ham_file_count))
print ('Total Distinct words are : '+ str(len(all_word_count)))
print ('Total Spam words are : '+ str(len(spam_word_count)))
print ('Total Ham words are : '+ str(len(ham_word_count)))