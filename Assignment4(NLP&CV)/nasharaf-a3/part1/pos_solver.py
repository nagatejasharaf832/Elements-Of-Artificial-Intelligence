###################################
# CS B551 Spring 2021, Assignment #3
#
# Your names and user ids:
# Nagatheja Sharaf - nasharaf@iu.edu
# Prasad Hegde     - phegde@iu.edu
# Akhil            - nyeniset@iu.edu
# (Based on skeleton code by D. Crandall)
#

import random
import math

# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#
class Solver:

    def __init__(self):
        # initialize all values
        self.mini_value = 0.0000001

        self.pos_count = {'adj': 0, 'adv': 0, 'adp': 0, 'conj': 0, 'det': 0,
                          'noun': 0, 'num': 0, 'pron': 0, 'prt': 0, 'verb': 0, 'x': 0, '.': 0}
        self.initial_count = {'adj': self.mini_value, 'adv': self.mini_value, 'adp': self.mini_value, 'conj': self.mini_value, 'det': self.mini_value, 'noun': self.mini_value,
                              'num': self.mini_value, 'pron': self.mini_value, 'prt': self.mini_value, 'verb': self.mini_value, 'x': self.mini_value, '.': self.mini_value}
        self.prob_pos_count = {'adj': 0, 'adv': 0, 'adp': 0, 'conj': 0, 'det': 0,
                               'noun': 0, 'num': 0, 'pron': 0, 'prt': 0, 'verb': 0, 'x': 0, '.': 0}
        self.pos = ['adj', 'adv', 'adp', 'conj', 'det',
                    'noun', 'num', 'pron', 'prt', 'verb', 'x', '.']

        self.prob_word_count = {}
        self.emission_count = {}
        self.word_count = {}
        self.gibbs = {}
        self.word_with_pos = {}
        self.bag_of_words = []
        self.trasition_count = {}
        self.next_line_reached = False

    # gives prosterior probability of all words in a sentence based on model type
    def posterior(self, model, sentence, label):
        """
        1. For simplified version for every word in a sentence calculate its emission probability
        Formulae: = sum(emission probability of words in a sentence)
        2. For Hidden Markov Model for every word in a sentence calculate its emission probability
        transition probability 
        if word is first word in a sentence then
        Formulae: sum(emission probability of words in a sentence)
        else
        Formulae: sum(emission probability of words in a sentence)+sum(transition probability of words in a sentence)
        3. For Gibbs algorithm for every word in a sentence calculate its emission probability
        transition probability and gibbs algorithm 
        if(length of sentecne is 1):
        Formulae: sum(emission probability of words in a sentence * (initial probability/sum(all initial probability values)))
        else if (word is first word in a sentence)
        Formulae: sum(emission probability of words in a sentence * (initial probability/sum(all initial probability values))*(transition probability)*(gibbs probability))
        else if (word is last word in a sentence)
        Formulae: (gibbs distribution * transition distribution)
        """
        if model == "Simple":
            result = 0
            for i in range(len(sentence)):
                result += math.log(
                    self.emission_distribution_prob(sentence[i])[label[i]])
            return result
        elif model == "HMM":
            result = 0
            for i in range(len(sentence)):
                if i == 0:
                    result += math.log(
                        self.emission_distribution_prob(sentence[i])[label[i]])
                else:
                    result += math.log(self.emission_distribution_prob(sentence[i])[label[i]]) \
                        + math.log(self.transition_distribution_prob(label[i])[label[i - 1]])

            return result

        elif model == "Complex":
            result = 0

            for i in range(len(sentence)):
                if len(sentence) == 1:
                    result += math.log(self.emission_distribution_prob(sentence[i])[label[i]]
                                       * (self.initial_count[label[i]] / sum(self.initial_count.values())))
                elif i == 0:
                    result += math.log(self.emission_distribution_prob(sentence[i])[label[i]]
                                       * (self.initial_count[label[i]] / sum(self.initial_count.values()))
                                       * self.transition_distribution_prob(label[i])[label[i + 1]]
                                       * self.gibbs_distribution_prob(sentence[i + 1], (label[i], label[i + 1])))
                elif i == len(sentence) - 1:
                    result += math.log(self.gibbs_distribution_prob(sentence[i], (label[i - 1], label[i]))
                                       * self.transition_distribution_prob(label[i - 1])[label[i]])
                else:
                    result += math.log(self.gibbs_distribution_prob(sentence[i], (label[i - 1], label[i]))
                                       * self.transition_distribution_prob(label[i - 1])[label[i]]
                                       * self.transition_distribution_prob(label[i])[label[i + 1]]
                                       * self.gibbs_distribution_prob(sentence[i + 1], (label[i], label[i + 1])))

            return result
        else:
            print("Unknown algo!")

    # calculate transition probabilites using transition values
    # This function will calculate probability of a pos(given) using all transition values
    transistion_prob = {}

    def transition_distribution_prob(self, p):
        if p not in self.transistion_prob.keys():
            temp_dict = {}
            # Formulae: transition values of given pos / sum(all transition values - transition value of given pos apperance)
            for i in self.pos:
                temp_dict[i] = self.trasition_count[p][i] / (
                    sum(self.trasition_count[p].values()) - self.trasition_count[p]['pos'])
            self.transistion_prob[p] = temp_dict
        return self.transistion_prob[p]

    # calculate emission probabilites using output of simplified algorithm values
    emission_prob = {}

    def emission_distribution_prob(self, word):

        if word not in self.emission_prob.keys():
            temp_dict = {}
            # Based on word pos count calculate emission probabilites
            for i in self.pos:
                if word in self.emission_count.keys():
                    temp_dict[i] = self.emission_count[word][i] / \
                        self.trasition_count[i]['pos']
                elif i == 'noun':
                    temp_dict[i] = 1 - (11 * self.mini_value)
                else:
                    temp_dict[i] = self.mini_value
            self.emission_prob[word] = temp_dict
        return self.emission_prob[word]

    # calculate gibbs probability
    def gibbs_distribution_prob(self, word, speeches):
        if word in self.gibbs.keys():
            if speeches in self.gibbs[word].keys():
                return self.gibbs[word][speeches] / sum([self.gibbs[word][k] for k in self.gibbs[word].keys() if k[0] == speeches[0]])

        return self.emission_distribution_prob(word)[speeches[1]]

    # start training data
    def train1(self):

        # fetch bag of words and add endofline when every line is ending
        for word, pos in (self.data):

            self.bag_of_words += (list(zip(pos, word)))
            self.bag_of_words.append(("endofline", "endofline"))

        # calculate transition count of all pos
        for idx, i in enumerate(self.bag_of_words):
            w = i[1]
            p = i[0]
            if(idx != len(self.bag_of_words)-1):
                p1 = self.bag_of_words[idx+1][0]
            # calculate until end of sentence is reached
            if(p != "endofline"):
                if(p1 != "endofline"):

                    if(p in self.trasition_count.keys()):
                        if(idx == 0 or self.next_line_reached == True and idx != len(self.bag_of_words)-1):
                            self.initial_count[p] += 1
                            self.next_line_reached = False
                        self.trasition_count[p][p1] += 1
                        self.trasition_count[p]["pos"] += 1
                    else:
                        self.trasition_count[p] = {'pos': 0, 'adj': self.mini_value, 'adv': self.mini_value, 'adp': self.mini_value, 'conj': self.mini_value, 'det': self.mini_value,
                                                   'noun': self.mini_value, 'num': self.mini_value, 'pron': self.mini_value, 'prt': self.mini_value, 'verb': self.mini_value, 'x': self.mini_value, '.': self.mini_value}
                        if(idx == 0 or self.next_line_reached == True and idx != len(self.bag_of_words)-1):
                            self.initial_count[p] += 1
                            self.next_line_reached = False
                        self.trasition_count[p][p1] += 1
                        self.trasition_count[p]["pos"] += 1
            else:
                self.next_line_reached = True

            # calculate word count for bag of words
            if(w != "endofline"):
                self.pos_count[p] += 1
                if w in self.word_count.keys():

                    self.word_count[w] = self.word_count[w]+1
                    self.word_with_pos[w][p] = self.word_with_pos[w][p]+1
                else:
                    self.word_count[w] = 1
                    self.word_with_pos[w] = {'adj': self.mini_value, 'adv': self.mini_value, 'adp': self.mini_value, 'conj': self.mini_value, 'det': self.mini_value,
                                             'noun': self.mini_value, 'num': self.mini_value, 'pron': self.mini_value, 'prt': self.mini_value, 'verb': self.mini_value, 'x': self.mini_value, '.': self.mini_value}
                    self.word_with_pos[w][p] += 1

        for i in self.word_count.keys():
            if(i not in self.prob_word_count.keys()):
                self.prob_word_count[i] = self.word_count[i] / \
                    len(self.word_count)

        for i in self.word_with_pos.keys():
            if i not in self.emission_count.keys():
                self.emission_count[i] = {'adj': self.mini_value, 'adv': self.mini_value, 'adp': self.mini_value, 'conj': self.mini_value, 'det': self.mini_value,
                                          'noun': self.mini_value, 'num': self.mini_value, 'pron': self.mini_value, 'prt': self.mini_value, 'verb': self.mini_value, 'x': self.mini_value, '.': self.mini_value}
                self.emission_count[i]["adj"] = self.word_with_pos[i]["adj"] / \
                    self.word_count[i]
                self.emission_count[i]["adv"] = self.word_with_pos[i]["adv"] / \
                    self.word_count[i]
                self.emission_count[i]["adp"] = self.word_with_pos[i]["adp"] / \
                    self.word_count[i]
                self.emission_count[i]["conj"] = self.word_with_pos[i]["conj"] / \
                    self.word_count[i]
                self.emission_count[i]["det"] = self.word_with_pos[i]["det"] / \
                    self.word_count[i]
                self.emission_count[i]["noun"] = self.word_with_pos[i]["noun"] / \
                    self.word_count[i]
                self.emission_count[i]["num"] = self.word_with_pos[i]["num"] / \
                    self.word_count[i]
                self.emission_count[i]["pron"] = self.word_with_pos[i]["pron"] / \
                    self.word_count[i]
                self.emission_count[i]["prt"] = self.word_with_pos[i]["prt"] / \
                    self.word_count[i]
                self.emission_count[i]["verb"] = self.word_with_pos[i]["verb"] / \
                    self.word_count[i]
                self.emission_count[i]["x"] = self.word_with_pos[i]["x"] / \
                    self.word_count[i]
                self.emission_count[i]["."] = self.word_with_pos[i]["."] / \
                    self.word_count[i]

        for i in self.pos_count.keys():
            self.prob_pos_count[i] = self.pos_count[i]/len(self.word_count)

        for i in self.word_with_pos.keys():
            if i not in self.emission_count.keys():
                self.emission_count[i] = {'adj': 0, 'adv': 0, 'adp': 0, 'conj': 0, 'det': 0, 'noun': 0,
                                          'num': 0, 'pron': 0, 'prt': 0, 'verb': 0, 'x': 0, '.': 0}
                self.emission_count[i]["adj"] = self.prob_pos_count["adj"]*(
                    self.word_with_pos[i]["adj"]/self.word_count[i])
                self.emission_count[i]["adv"] = self.prob_pos_count["adv"]*(
                    self.word_with_pos[i]["adv"]/self.word_count[i])
                self.emission_count[i]["adp"] = self.prob_pos_count["adp"]*(
                    self.word_with_pos[i]["adp"]/self.word_count[i])
                self.emission_count[i]["conj"] = self.prob_pos_count["conj"]*(
                    self.word_with_pos[i]["conj"]/self.word_count[i])
                self.emission_count[i]["det"] = self.prob_pos_count["det"]*(
                    self.word_with_pos[i]["det"]/self.word_count[i])
                self.emission_count[i]["noun"] = self.prob_pos_count["noun"]*(
                    self.word_with_pos[i]["noun"]/self.word_count[i])
                self.emission_count[i]["num"] = self.prob_pos_count["num"]*(
                    self.word_with_pos[i]["num"]/self.word_count[i])
                self.emission_count[i]["pron"] = self.prob_pos_count["pron"]*(
                    self.word_with_pos[i]["pron"]/self.word_count[i])
                self.emission_count[i]["prt"] = self.prob_pos_count["prt"]*(
                    self.word_with_pos[i]["prt"]/self.word_count[i])
                self.emission_count[i]["verb"] = self.prob_pos_count["verb"]*(
                    self.word_with_pos[i]["verb"]/self.word_count[i])
                self.emission_count[i]["x"] = self.prob_pos_count["x"] * \
                    (self.word_with_pos[i]["x"]/self.word_count[i])
                self.emission_count[i]["."] = self.prob_pos_count["."] * \
                    (self.word_with_pos[i]["."]/self.word_count[i])

    def train(self, data):
        self.data = data
        self.train1()

    # Functions for each algorithm. Right now this just returns nouns -- fix this!
    #

    def simplified(self, sentence):
        lis = []
        for i in sentence:
            if i in self.emission_count.keys():
                a_dictionary = self.emission_count[i]
            else:
                a_dictionary = {'adj': 0, 'adv': 0, 'adp': 0, 'conj': 0, 'det': 0,
                                'noun': 1, 'num': 0, 'pron': 0, 'prt': 0, 'verb': 0, 'x': 0, '.': 0}
            max_key = max(a_dictionary, key=a_dictionary.get)
            lis.append(max_key)
        return lis

    def hmm_viterbi(self, sentence):
        # initialize with 0s  in vi table and which table
        vi_table = [[0 for i in range(12)] for t in range(len(sentence))]
        which_table = [[0 for i in range(12)] for t in range(len(sentence))]
        result = []
        for i in range(0, len(sentence)):
            count = 0
            for p in self.pos:
                # if the word in sentence is first word then
                # formulae  = emission probabilites-initial prob
                if i == 0:
                    vi_table[i][count] = -math.log(self.emission_distribution_prob(sentence[i])[p]) \
                        - math.log((self.initial_count[p] / sum(self.initial_count.values())))
                    count = count + 1
                else:
                    # formulae = transition probability - emission prob
                    q = list(range(0, 12))
                    vi_tablevalues = [vi_table[i - 1][l]
                                      - math.log(self.transition_distribution_prob(p2)[p])
                                      - math.log(self.emission_distribution_prob(sentence[i])[p])
                                      for l, p2 in zip(q, self.pos)]
                    # select min as we are taking log values among all vi table values
                    cost = min(vi_tablevalues)
                    vi_table[i][count] = cost
                    # store the index of that min value above into which table
                    which_table[i][count] = self.pos[vi_tablevalues.index(
                        cost)]
                    count = count + 1
        # back tracking
        result = [""]*len(sentence)
        last = self.pos[vi_table[len(
            sentence) - 1].index(min(vi_table[len(sentence) - 1]))]
        result[-1] = last
        for i in range(len(sentence)-1, 0, -1):
            m = vi_table[i].index(min(vi_table[i]))
            result[i-1] = which_table[i][m]
        return result

    # complex monte carlo markov chain
    def complex_mcmc(self, sentence):
        count = []
        sample = []
        sen_len_pos_tags = {}
        prob = {}

        for i in range(0, len(sentence)):
            for p in self.pos:
                sen_len_pos_tags[p] = 0
            count.append(sen_len_pos_tags)
            sen_len_pos_tags = {}

        for i in range(0, len(sentence)):
            sample.append("noun")

        iterations = 1000
        for i in range(iterations):
            for j in range(len(sample)):
                # for every pos calculate prob of every word
                for p in self.pos:
                    # if sample =1
                    # formulae = emission prob * initial count / sum(initial count values)
                    if(len(sample) == 1):
                        prob[p] = self.emission_distribution_prob(sentence[j])[p] * \
                            (self.initial_count[p] /
                             sum(self.initial_count.values()))
                    # if this is first sample then
                    # formulae = emission prob * initial count / sum(initial count values) * transition prob * gibbs prob
                    elif j == 0:
                        prob[p] = self.emission_distribution_prob(sentence[j])[p] * \
                            (self.initial_count[p] / sum(self.initial_count.values())) * \
                            self.transition_distribution_prob(p)[sample[j + 1]] * \
                            self.gibbs_distribution_prob(
                                sentence[j + 1], (p, sample[j + 1]))
                    # if this is last sample then
                    # formulae  = gibbs prob * transition prob
                    elif j == len(sample) - 1:
                        prob[p] = self.gibbs_distribution_prob(sentence[j], (sample[j - 1], p)) * \
                            self.transition_distribution_prob(sample[j - 1])[p]

                    else:
                        prob[p] = self.gibbs_distribution_prob(sentence[j], (sample[j - 1], p)) * \
                            self.transition_distribution_prob(sample[j - 1])[p] * \
                            self.transition_distribution_prob(p)[sample[j + 1]] * \
                            self.gibbs_distribution_prob(
                                sentence[j + 1], (p, sample[j + 1]))

                probs = {v: float(prob[v]) / sum(prob.values())
                         for v in self.pos}

                # sample the probs
                rand = random.random()
                num = 0
                for p in self.pos:
                    num += probs[p]
                    if rand < num:
                        sample[j] = p
                        break
                # first half of iterations
                if i > iterations / 2:
                    for k in range(len(sample)):
                        count[k][sample[k]] += 1
        result = []
        for i in range(len(sample)):
            pos = "noun"
            max = 0
            for p in self.pos:
                if count[i][p] >= max:
                    max = count[i][p]
                    pos = p
            result.append(pos)
        return result

    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself.
    # It should return a list of part-of-speech labelings of the sentence, one
    #  part of speech per word.
    #

    def solve(self, model, sentence):
        if model == "Simple":
            return self.simplified(sentence)
        elif model == "HMM":
            return self.hmm_viterbi(sentence)
        elif model == "Complex":
            return self.complex_mcmc(sentence)
        else:
            print("Unknown algo!")
