#NLP Assignment 1 - Niranjana Kandavel - 21st September 2016
import os
import math
import pickle
import sys

with open('stop_word_list.txt', "r") as word_list:
    stop_words = word_list.read().split()

#file_path = sys.argv[1]
file_path = '/home/ninja/PycharmProjects/NlpAssign1/spamham/dev'
fout = open('nboutput.txt','w')

#read the nbmodel.txt
words_count = pickle.load(open("nbmodel.txt", "rb"))

#de-nesting the nested dictionary
spam_word_dict = words_count["spam"]
ham_word_count = words_count["ham"]
all_word_count = words_count["all"]
probality_files = words_count["file"]

#Size of Vocabulary
V_size = len(all_word_count)

#get the values needed for probablity calculation
spam_file_prob = probality_files["spam"]
ham_file_prob = probality_files["ham"]
spam_words_tot = probality_files["spamwords"]
ham_words_tot = probality_files["hamwords"]

probablity_spam = 0
probablity_ham = 0
act_spam_count = 0
act_ham_count = 0
cal_spam_count =0
cal_ham_count =0
match = 0
mismatch = 0
ham_match = 0
spam_match = 0
isham = 0


#scan the files recursively and caculate the probablity of spam and ham files
for root, dirs, files in os.walk(file_path):
    for file in files:
        if file.endswith('.txt'):
            fullfilename = os.path.join(root, file)
            probablity_spam = 0
            probablity_ham = 0
            for w in open(fullfilename, "r", encoding="latin1").read().split():
                if w in all_word_count:
                    if w not in stop_words:
                        if w in spam_word_dict:
                            probablity_spam += math.log((spam_word_dict[w] + 1)/ (spam_words_tot + V_size))
                        else:
                            probablity_spam += math.log(1/(spam_words_tot + V_size))
                        if w in ham_word_count:
                            probablity_ham += math.log((ham_word_count[w] + 1)/ (ham_words_tot + V_size))
                        else:
                            probablity_ham += math.log(1 / (ham_words_tot + V_size))
            probablity_spam += math.log(spam_file_prob)
            probablity_ham += math.log(ham_file_prob)
            isham = 0
            if probablity_spam > probablity_ham:
                fout.write("SPAM"+" "+fullfilename+"\n")
                cal_spam_count += 1
            else:
                fout.write("HAM" + " " + fullfilename+"\n")
                cal_ham_count += 1
                isham += 1

        if file.endswith('ham.txt'):
            act_ham_count += 1
            if (isham == 1):
                match += 1
                ham_match += 1
            else:
                mismatch += 1
        if file.endswith('spam.txt'):
            act_spam_count += 1
            if (isham == 1):
                mismatch += 1
            else:
                match += 1
                spam_match += 1

#ham calculation
print ("Actual Ham Files Count : "+str(act_ham_count))
print ("Calculated Ham Files Count : "+str(ham_match))

pre_ham = ham_match*100/cal_ham_count
print("Ham Precision : "+str(pre_ham))
recall_ham = ham_match*100/act_ham_count
print("Ham Recall : "+str(recall_ham))
f1_ham = (2 * pre_ham * recall_ham) / (pre_ham + recall_ham)
print("Ham F1 score : "+str(f1_ham))

#spam calculation
print ("Actual Spam Files Count : "+str(act_spam_count))
print ("Calcaulated Spam Files Count : "+str(spam_match))

pre_spam = spam_match*100/cal_spam_count
print("Spam Precision : "+str(pre_spam))
recall_spam = spam_match*100/act_spam_count
print("Spam Recall : "+str(recall_spam))
f1_spam = (2 * pre_spam * recall_spam) / (pre_spam + recall_spam)
print("Spam F1 Score : "+str(f1_spam))

#few other calculation(not part of assignmnet)
accuracy = match/(act_ham_count+act_spam_count)
print("Accuracy : "+str(accuracy))
print ("Total Matched File Count : "+str(match))
print  ("Total Mismatched File Count : "+str(mismatch))