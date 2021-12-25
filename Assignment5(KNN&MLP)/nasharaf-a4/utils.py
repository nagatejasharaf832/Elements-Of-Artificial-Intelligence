# utils.py: Utility file for implementing helpful utility functions used by the ML algorithms.
#
# Submitted by: [enter your full name here] -- [enter your IU username here]
#
# Based on skeleton code by CSCI-B 551 Fall 2021 Course Staff

import numpy as np
import math
from numpy.core.fromnumeric import shape

# https://www.geeksforgeeks.org/calculate-the-euclidean-distance-using-numpy/
def euclidean_distance(x1, x2):
    """
    Computes and returns the Euclidean distance between two vectors.

    Args:
        x1: A numpy array of shape (n_features,).
        x2: A numpy array of shape (n_features,).
    """
    e = np.linalg.norm(x1-x2)
    return(e.tolist())
    raise NotImplementedError('This function must be implemented by the student.')

# https://www.geeksforgeeks.org/calculate-the-euclidean-distance-using-numpy/
def manhattan_distance(x1, x2):
    """
    Computes and returns the Manhattan distance between two vectors.

    Args:
        x1: A numpy array of shape (n_features,).
        x2: A numpy array of shape (n_features,).
    """
    e = np.abs(x1 - x2).sum()
    return(e.tolist())
    raise NotImplementedError('This function must be implemented by the student.')


def identity(x, derivative = False):
    """
    Computes and returns the identity activation function of the given input data x. If derivative = True,
    the derivative of the activation function is returned instead.

    Args:
        x: A numpy array of shape (n_samples, n_hidden).
        derivative: A boolean representing whether or not the derivative of the function should be returned instead.
    """
    x = np.array(x)
    if(not derivative):
        return x
    else:
        return np.ones(x.shape)
    raise NotImplementedError('This function must be implemented by the student.')

# https://machinelearningmastery.com/a-gentle-introduction-to-sigmoid-function/
def sigmoid(x, derivative = False):
    """
    Computes and returns the sigmoid (logistic) activation function of the given input data x. If derivative = True,
    the derivative of the activation function is returned instead.

    Args:
        x: A numpy array of shape (n_samples, n_hidden).
        derivative: A boolean representing whether or not the derivative of the function should be returned instead.
    """
    # formulae -  1/1+exp(-x)
    x = np.array(x)
    if(not(derivative)):
        return 1 / (1 + np.exp(-x))
    else:
        return x * (1 - x)


    raise NotImplementedError('This function must be implemented by the student.')

# https://machinelearningmastery.com/a-gentle-introduction-to-sigmoid-function/
def tanh(x, derivative = False):
    """
    Computes and returns the hyperbolic tangent activation function of the given input data x. If derivative = True,
    the derivative of the activation function is returned instead.

    Args:
        x: A numpy array of shape (n_samples, n_hidden).
        derivative: A boolean representing whether or not the derivative of the function should be returned instead.
    """
    # formuale - numpy has tanh np.tanh(x)
    x = np.array(x)
    if(not(derivative)):
        return np.tanh(x)
    else:
        return 1 - np.tanh(x) ** 2

    raise NotImplementedError('This function must be implemented by the student.')

# https://machinelearningmastery.com/rectified-linear-activation-function-for-deep-learning-neural-networks
def relu(x, derivative = False):
    """
    Computes and returns the rectified linear unit activation function of the given input data x. If derivative = True,
    the derivative of the activation function is returned instead.

    Args:
        x: A numpy array of shape (n_samples, n_hidden).
        derivative: A boolean representing whether or not the derivative of the function should be returned instead.
    """
    # formulae = if derivative maximum(list:x) else boolean(x>1)
    x = np.array(x)
    if(not(derivative)):
        return np.maximum(0, x)
    else:
        return (x > 0) * 1

    raise NotImplementedError('This function must be implemented by the student.')


def softmax(x, derivative = False):
    x = np.clip(x, -1e100, 1e100)
    if not derivative:
        c = np.max(x, axis = 1, keepdims = True)
        return np.exp(x - c - np.log(np.sum(np.exp(x - c), axis = 1, keepdims = True)))
    else:
        return softmax(x) * (1 - softmax(x))

# https://machinelearningmastery.com/cross-entropy-for-machine-learning/
def cross_entropy(y, p):
    """
    Computes and returns the cross-entropy loss, defined as the negative log-likelihood of a logistic model that returns
    p probabilities for its true class labels y.

    Args:
        y:
            A numpy array of shape (n_samples, n_outputs) representing the one-hot encoded target class values for the
            input data used when fitting the model.
        p:
            A numpy array of shape (n_samples, n_outputs) representing the predicted probabilities from the softmax
            output activation function.
    """
    # formulae- – sum x in X P(x) * log(P(x))
    y = y.tolist()
    for id,val in enumerate(y):
        if(val) == 0.0:
            y[id] = 1.0
        if(val) == 0:
            y[id] = 1
    return -sum([p[i]*math.log2(y[i]) for i in range(len(p))])

    raise NotImplementedError('This function must be implemented by the student.')

# https://machinelearningmastery.com/why-one-hot-encode-data-in-machine-learning/
def one_hot_encoding(y):
    """
    Converts a vector y of categorical target class values into a one-hot numeric array using one-hot encoding: one-hot
    encoding creates new binary-valued columns, each of which indicate the presence of each possible value from the
    original data.

    Args:
        y: A numpy array of shape (n_samples,) representing the target class values for each sample in the input data.

    Returns:
        A numpy array of shape (n_samples, n_outputs) representing the one-hot encoded target class values for the input
        data. n_outputs is equal to the number of unique categorical class values in the numpy array y.
    """
    # formulae - 
    # y = np.array(y)
    print(y,y[0],y[1])
    y2 = np.array(y)
    y =y2[0]
    y1 = y2[1]
    x = np.array([np.eye(i) for i in np.unique(y1)])
    y=y.tolist()
    print(x,y)
    return(x.tolist()[0][y])
    raise NotImplementedError('This function must be implemented by the student.')
