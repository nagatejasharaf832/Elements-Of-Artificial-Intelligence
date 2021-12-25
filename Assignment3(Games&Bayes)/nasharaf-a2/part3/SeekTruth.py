# SeekTruth.py : Classify text objects into two categories
#
# John Holt aka holtjohn
# - with sathup & nasharaf 
#
# Based on skeleton code by D. Crandall, October 2021
#

import sys

def load_file(filename):
    objects=[]
    labels=[]
    with open(filename, "r") as f:
        for line in f:
            parsed = line.strip().split(' ',1)
            labels.append(parsed[0] if len(parsed)>0 else "")
            objects.append(parsed[1] if len(parsed)>1 else "")

    return {"objects": objects, "labels": labels, "classes": list(set(labels))}

# Cleans up the words in the data sets by doing the following:
# - Sets to lower case
# - Removes all characters not from a-z
# - Removes s
#
def word_cleaner(word):
    clean_word = ""
    for letter in word.lower():
        if letter in ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','t','u','v','w','x','y','z']:
            clean_word+=letter
    return clean_word

# Classifier : Train and apply a bayes net classifier
#
# This function takes a train_data dictionary that has three entries:
#        train_data["objects"] is a list of strings corresponding to reviews
#        train_data["labels"] is a list of strings corresponding to ground truth labels for each review
#        train_data["classes"] is the list of possible class names (always two)
#
# and a test_data dictionary that has objects and classes entries in the same format as above. It
# returns a list of the same length as test_data["objects"], where the i-th element of the result
# list is the estimated classlabel for test_data["objects"][i]
#
def classifier(train_data, test_data):
    word_count = {}
    truth_word_count = {}
    truth_comment_count = 0
    true_word_total = 0
    deceptive_word_count = {}
    deceptive_comment_count = 0
    deceptive_word_total = 0
    for i in range(len(train_data["objects"])):
        if train_data["labels"][i] == "truthful":
            truth_comment_count+=1
        else:
            deceptive_comment_count+=1
        for dirty_word in train_data["objects"][i].split():
            word = word_cleaner(dirty_word)
            #Removes undeservedly influential words to improve accuracy
            if word in ['i','to','we','at','ervice']:
                continue
            if word in word_count:
                word_count[word]+=1
            else:
                word_count[word]=1
            if train_data["labels"][i]=="truthful":
                if word in truth_word_count:
                    truth_word_count[word]+=1
                    true_word_total+=1
                else:
                    truth_word_count[word]=1
                    true_word_total+=1
            else:
                if word in deceptive_word_count:
                    deceptive_word_count[word]+=1
                    deceptive_word_total+=1
                else:
                    deceptive_word_count[word]=1
                    deceptive_word_total+=1
    prob_dict = {}
    for key in truth_word_count:
        if key in deceptive_word_count:
            prob_dict[key] = (truth_word_count[key]/true_word_total)/(deceptive_word_count[key]/deceptive_word_total)
    test_data['labels'] = []

    for i in range(len(test_data["objects"])):
        truthiness = (truth_comment_count/len(train_data["objects"]))/(deceptive_comment_count/len(train_data["objects"]))
        for dirty_word in test_data["objects"][i].split():
            word = word_cleaner(dirty_word)
            if word in prob_dict:
                truthiness = truthiness*prob_dict[word]
        if truthiness > 1:
            test_data["labels"].append('truthful')

        else:
            test_data["labels"].append('deceptive')
    return test_data["labels"]

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Usage: classify.py train_file.txt test_file.txt")

    (_, train_file, test_file) = sys.argv
    # Load in the training and test datasets. The file format is simple: one object
    # per line, the first word one the line is the label.
    train_data = load_file(train_file)
    test_data = load_file(test_file)
    if(sorted(train_data["classes"]) != sorted(test_data["classes"]) or len(test_data["classes"]) != 2):
        raise Exception("Number of classes should be 2, and must be the same in test and training data")

    # make a copy of the test data without the correct labels, so the classifier can't cheat!
    test_data_sanitized = {"objects": test_data["objects"], "classes": test_data["classes"]}

    results= classifier(train_data, test_data_sanitized)

    # calculate accuracy
    correct_ct = sum([ (results[i] == test_data["labels"][i]) for i in range(0, len(test_data["labels"])) ])
    print("Classification accuracy = %5.2f%%" % (100.0 * correct_ct / len(test_data["labels"])))
