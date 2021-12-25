# k_nearest_neighbors.py: Machine learning implementation of a K-Nearest Neighbors classifier from scratch.
#
# Submitted by: [enter your full name here] -- [enter your IU username here]
#
# Based on skeleton code by CSCI-B 551 Fall 2021 Course Staff

# import numpy as np
import math
# from numpy.core.fromnumeric import sort
from utils import euclidean_distance, manhattan_distance


class KNearestNeighbors:
    """
    A class representing the machine learning implementation of a K-Nearest Neighbors classifier from scratch.

    Attributes:
        n_neighbors
            An integer representing the number of neighbors a sample is compared with when predicting target class
            values.

        weights
            A string representing the weight function used when predicting target class values. The possible options are
            {'uniform', 'distance'}.

        _X
            A numpy array of shape (n_samples, n_features) representing the input data used when fitting the model and
            predicting target class values.

        _y
            A numpy array of shape (n_samples,) representing the true class values for each sample in the input data
            used when fitting the model and predicting target class values.

        _distance
            An attribute representing which distance metric is used to calculate distances between samples. This is set
            when creating the object to either the euclidean_distance or manhattan_distance functions defined in
            utils.py based on what argument is passed into the metric parameter of the class.

    Methods:
        fit(X, y)
            Fits the model to the provided data matrix X and targets y.

        predict(X)
            Predicts class target values for the given test data matrix X using the fitted classifier model.
    """

    def __init__(self, n_neighbors = 5, weights = 'uniform', metric = 'l2'):
        # Check if the provided arguments are valid
        if weights not in ['uniform', 'distance'] or metric not in ['l1', 'l2'] or not isinstance(n_neighbors, int):
            raise ValueError('The provided class parameter arguments are not recognized.')

        # Define and setup the attributes for the KNearestNeighbors model object
        self.n_neighbors = n_neighbors
        self.weights = weights
        self._X = None
        self._y = None
        self._distance = euclidean_distance if metric == 'l2' else manhattan_distance

    def fit(self, X, y):
        """
        Fits the model to the provided data matrix X and targets y.

        Args:
            X: A numpy array of shape (n_samples, n_features) representing the input data.
            y: A numpy array of shape (n_samples,) representing the true class values for each sample in the input data.

        Returns:
            None.
        """
        self._X = X
        self._y = y

    def predict(self, X):
        """
        Predicts class target values for the given test data matrix X using the fitted classifier model.

        Args:
            X: A numpy array of shape (n_samples, n_features) representing the test data.

        Returns:
            A numpy array of shape (n_samples,) representing the predicted target class values for the given test data.
        """
        all_dis = []
        sorted_list =[]
        # loop test and train data set
        for test in X:
            for idx,train in enumerate(self._X):
                e1 = self._distance(test,train)
                # calculate distance based on uniform or not
                if(e1)!=0:
                    if(self.weights == "distance"):
                        e1 = -1/e1
                    else:
                        e1 = e1
                else:
                    e1 = -math.inf

                # append distance and category of that index
                all_dis.append(tuple((e1,self._y[idx])))
            # https://flaviocopes.com/how-to-sort-array-of-objects-by-property-javascript/
            # sort all_dis based on shortest distance
            all_dis.sort(key=lambda tup: tup[0])
            # slice the array based on neighbors
            sorted_list.append(all_dis[:self.n_neighbors])
            all_dis = []

        cat = []
        final_cat_list = []
        # append final categories to list
        for k in sorted_list:
            for k1 in k:
                cat.append(k1[1])
            final_cat_list.append(cat)
            cat = []
        # find mode for final categories 
        # https://flaviocopes.com/how-to-sort-array-of-objects-by-property-javascript/
        p =[max(i, key = i.count) for i in final_cat_list]
        return(p)