#!/usr/bin/python
#
# Perform optical character recognition, usage:
#     python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png
# 
# Authors: 
# Nagatheja Sharaf - nasharaf@iu.edu
# Prasad Hegde     - phegde@iu.edu
# Akhil            - nyeniset@iu.edu
#
# (based on skeleton code by D. Crandall, Oct 2020)
#

from PIL import Image, ImageDraw, ImageFont
import sys
import copy,math

CHARACTER_WIDTH=14
CHARACTER_HEIGHT=25
TRAIN_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "

def load_letters(fname):
    im = Image.open(fname)
    px = im.load()
    (x_size, y_size) = im.size
    result = []
    for x_beg in range(0, int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH, CHARACTER_WIDTH):
        result += [ [ "".join([ '*' if px[x, y] < 1 else ' ' for x in range(x_beg, x_beg+CHARACTER_WIDTH) ]) for y in range(0, CHARACTER_HEIGHT) ], ]
    return result

def load_training_letters(fname):
    TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    letter_images = load_letters(fname)
    return { TRAIN_LETTERS[i]: letter_images[i] for i in range(0, len(TRAIN_LETTERS) ) }

# This function stores reads the input file and return a list of sentences
def read_data(fname):
    exemplars = []
    file = open(fname, 'r')
    for line in file:
        data = tuple([w for w in line.split()])
        exemplars += [ " ".join(data) ]
    return exemplars

#####
# main program
if len(sys.argv) != 4:
    raise Exception("Usage: python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png")

(train_img_fname, train_txt_fname, test_img_fname) = sys.argv[1:]
train_letters = load_training_letters(train_img_fname)

test_letters = load_letters(test_img_fname)

# This method is used to calculate the emission_probability 
def emission_probability(test,train):
    Letterprob = {}
    for x in TRAIN_LETTERS:
        space_match, asterick_match, asterick_mismatch,space_mismatch = 0, 0, 0, 0
        for i in range(0, len(test)):
            for j in range(0, len(test[i])):
                if train[x][i][j] == '*' and test[i][j] == '*':  # checks if there is '*' in both train and test
                    asterick_match += 1
                elif train[x][i][j] == ' ' and test[i][j] == ' ': # checks if there is ' ' in both train and test
                    space_match += 1
                elif train[x][i][j] == '*' and test[i][j] == ' ': # checks if there is '*' in train and ' ' test
                    asterick_mismatch += 1
                else:                                             # checks if there is ' ' in train and '*' test
                    space_mismatch += 1

        # We are calculating the probabilities of each character in test by assuming there will be some noise
        prob = math.pow(0.9, asterick_match) * math.pow(0.1, space_mismatch) * math.pow(0.6,space_match) * math.pow(0.4, asterick_mismatch)
        Letterprob.update({x:prob})
        prob = 0
    return Letterprob

# This method generates the the transition table for all train characters
def transitionMatrix(lines,TRAIN_LETTERS):
    # Creating a dictionary for transition table
    dictOfWords = { char : { c:0.00000000000001 for c in TRAIN_LETTERS+'$'} for char in TRAIN_LETTERS }
    
    # checking the transitions for each character and increasing the count for each transitions
    for line in lines:
        for i in range(len(line)):
            if line[i] not in TRAIN_LETTERS:
                continue
            elif i == 0:
                dictOfWords[line[i]]['$'] += 1 
            elif line[i-1] in TRAIN_LETTERS:
                dictOfWords[line[i-1]][line[i]] += 1
    # Calculating the probabilities for transitions
    for i in range(len(dictOfWords)):
        total_trans = sum(dictOfWords[TRAIN_LETTERS[i]].values())
        for j in dictOfWords[TRAIN_LETTERS[i]]:
            dictOfWords[TRAIN_LETTERS[i]][j] /= total_trans
    return dictOfWords

# This method recognizes the text by using simple bayes net
def simple():
    result = []
    for letter in test_letters:
        simple_prob = emission_probability(letter, train_letters)
        result.append(max(simple_prob, key=simple_prob.get))
    return result

# This method recognizes the text by using Viterbi
def hmm(train_letters, test_letters):

    # Creating tables for viterbi and which tables
    v_table = [[0 for i in range(len(TRAIN_LETTERS))] for t in range(len(test_letters))]
    which_table = [[0 for i in range(len(TRAIN_LETTERS))] for t in range(len(test_letters))]

    lines=read_data(train_txt_fname)
    trans_matrix=transitionMatrix(lines,TRAIN_LETTERS)

    result = []
    for i in range(0, len(test_letters)):
        v_col = 0
        emission = emission_probability(test_letters[i], train_letters)
        for train in TRAIN_LETTERS:
            if i == 0:
                #calculating the initial probabilities
                v_table[i][v_col] = - 10* math.log(emission[train]) - math.log(trans_matrix[train]['$'])
                v_col += 1
            else:
                # Calculating the probabilites of viterbi table by using transition tables
                q = list(range(len(TRAIN_LETTERS)))
                v_tablevalues = {}
                for col,char in zip(q,TRAIN_LETTERS):
                    v_tablevalues.update({char:v_table[i - 1][col] - math.log(trans_matrix[char][train]) -  10* math.log(emission[train])})
                v_char = min(v_tablevalues,key=v_tablevalues.get)
                cost = v_tablevalues[v_char]
                # storing the minimum value in viterbi table
                v_table[i][v_col] = cost
                # Storing the characters in which table
                which_table[i][v_col] = v_char
                v_col += 1
                
    # Back tracking the viterbi table by using which table
    result = ['']*len(test_letters)
    result[-1]=TRAIN_LETTERS[(v_table[len(test_letters)-1].index(min(v_table[len(test_letters)-1])))]
    for i in range(len(test_letters)-1,0,-1):
        m=v_table[i].index(min(v_table[i]))
        result[i-1] = which_table[i][m]
    return result

simple_res = simple()
hmm_res = hmm(train_letters,test_letters)

# The final two lines of your output should look something like this:
print("Simple: " + "".join(simple_res))
print("   HMM: " + "".join(hmm_res))
