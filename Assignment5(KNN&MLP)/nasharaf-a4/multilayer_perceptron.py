# multilayer_perceptron.py: Machine learning implementation of a Multilayer Perceptron classifier from scratch.
#
# Submitted by: [enter your full name here] -- [enter your IU username here]
#
# Based on skeleton code by CSCI-B 551 Fall 2021 Course Staff

from re import S
import numpy as np
import random
from utils import identity, sigmoid, tanh, relu, softmax, cross_entropy, one_hot_encoding


class MultilayerPerceptron:
    """
    A class representing the machine learning implementation of a Multilayer Perceptron classifier from scratch.

    Attributes:
        n_hidden
            An integer representing the number of neurons in the one hidden layer of the neural network.

        hidden_activation
            A string representing the activation function of the hidden layer. The possible options are
            {'identity', 'sigmoid', 'tanh', 'relu'}.

        n_iterations
            An integer representing the number of gradient descent iterations performed by the fit(X, y) method.

        learning_rate
            A float representing the learning rate used when updating neural network weights during gradient descent.

        _output_activation
            An attribute representing the activation function of the output layer. This is set to the softmax function
            defined in utils.py.

        _loss_function
            An attribute representing the loss function used to compute the loss for each iteration. This is set to the
            cross_entropy function defined in utils.py.

        _loss_history
            A Python list of floats representing the history of the loss function for every 20 iterations that the
            algorithm runs for. The first index of the list is the loss function computed at iteration 0, the second
            index is the loss function computed at iteration 20, and so on and so forth. Once all the iterations are
            complete, the _loss_history list should have length n_iterations / 20.

        _X
            A numpy array of shape (n_samples, n_features) representing the input data used when fitting the model. This
            is set in the _initialize(X, y) method.

        _y
            A numpy array of shape (n_samples, n_outputs) representing the one-hot encoded target class values for the
            input data used when fitting the model.

        _h_weights
            A numpy array of shape (n_features, n_hidden) representing the weights applied between the input layer
            features and the hidden layer neurons.

        _h_bias
            A numpy array of shape (1, n_hidden) representing the weights applied between the input layer bias term
            and the hidden layer neurons.

        _o_weights
            A numpy array of shape (n_hidden, n_outputs) representing the weights applied between the hidden layer
            neurons and the output layer neurons.

        _o_bias
            A numpy array of shape (1, n_outputs) representing the weights applied between the hidden layer bias term
            neuron and the output layer neurons.

    Methods:
        _initialize(X, y)
            Function called at the beginning of fit(X, y) that performs one-hot encoding for the target class values and
            initializes the neural network weights (_h_weights, _h_bias, _o_weights, and _o_bias).

        fit(X, y)
            Fits the model to the provided data matrix X and targets y.

        predict(X)
            Predicts class target values for the given test data matrix X using the fitted classifier model.
    """
    # https://machinelearningmastery.com/implement-backpropagation-algorithm-scratch-python/
    # calculate random weights based on the desired array sizes
    def random_weights(self, x, y):
        return [[2 * random.random() - 1 for i in range(x)] for j in range(y)]

    def __init__(self, n_hidden=16, hidden_activation='sigmoid', n_iterations=1000, learning_rate=0.01):
        # Create a dictionary linking the hidden_activation strings to the functions defined in utils.py
        activation_functions = {'identity': identity,
                                'sigmoid': sigmoid, 'tanh': tanh, 'relu': relu}

        # Check if the provided arguments are valid
        if not isinstance(n_hidden, int) \
                or hidden_activation not in activation_functions \
                or not isinstance(n_iterations, int) \
                or not isinstance(learning_rate, float):
            raise ValueError(
                'The provided class parameter arguments are not recognized.')

        # Define and setup the attributes for the MultilayerPerceptron model object
        self.n_hidden = n_hidden
        self.hidden_activation = activation_functions[hidden_activation]
        self.n_iterations = n_iterations
        self.learning_rate = learning_rate
        self.input_layer = 5
        self.classes_number = 3
        self._output_activation = softmax
        self._loss_function = cross_entropy
        self._loss_history = []
        self._X = None
        self._y = None
        self._h_weights = None
        self._o_weights = None
        self.derivada = {
            'sigmoid': (lambda x: x*(1-x)),
            'tanh': (lambda x: 1-x**2),
            'relu': (lambda x: 1 * (x > 0)),
            'identity': (lambda x: 1 * (x))
        }
        self.deriv = self.derivada[hidden_activation]

    def _initialize(self, X, y):
        """
        Function called at the beginning of fit(X, y) that performs one hot encoding for the target class values and
        initializes the neural network weights (_h_weights, _h_bias, _o_weights, and _o_bias).

        Args:
            X: A numpy array of shape (n_samples, n_features) representing the input data.
            y: A numpy array of shape (n_samples,) representing the true class values for each sample in the input data.

        Returns:
            None.
        """
        self._X = X
        self._h_weights = []
        count_epoch = 1
        self.layer2 = 0
        self.W0 = []
        self.WC = []
        self.W2 = []
        self.W3 = []
        self.sum_err = 0
        self._loss_history = []
        self.h_bias = 0.1
        self.o_bias = 0.2
        # initialize weigths
        self._h_weights = self.random_weights(len(X[0]), self.n_hidden)
        self._o_weights = self.random_weights(self.n_hidden, max(y)+1)
        # loop unitl n iterations
        while(count_epoch <= self.n_iterations//len(y)):
            self.sum_err = 0
            self.layer2 = 0
            # loop train data
            for idx, inputs in enumerate(X):
                # feed forward propogation
                for idx1 in range(self.n_hidden):
                    # first layer farword propogation
                    self.layer1 = sum(inputs * self._h_weights[idx1])+self.h_bias
                    self.W0.append(self.layer1)
                for idx2 in range(max(y)+1):
                    # ouput layer farword propogation
                    for id1, j in enumerate(self.W0):
                        self.layer2 += (self.hidden_activation(j)
                                        * self._o_weights[idx2][id1])+self.o_bias
                    self.W2.append(self.layer2)
                    self.layer2 = 0
                # output values
                self.W3.append(self.W2)
                self.WC.append(self.W2)
                # error = target-probability
                err = one_hot_encoding((y[idx],max(y)+1))-softmax(self.W3)
                err = err[0]
                self.sum_err+=sum(err)
                self.W3 = np.array(self.W3)
                # bias values
                x_cap  = np.dot(err, self.W3.T)
                self.W3 = self.W3.tolist()
                x_cap = x_cap[0]
                # back propogation and updating weights
                for id2,wei in enumerate(self._o_weights):
                    for id3,wei1 in enumerate(wei):
                        self._o_weights[id2][id3]= wei1 - self.learning_rate*self.sum_err*sum(self.hidden_activation(self.W2,derivative=True))
                for we1,wei in enumerate(self._h_weights):
                    for we2,wei1 in enumerate(wei):
                        self._h_weights[we1][we2]= wei1 - self.learning_rate*self.sum_err*sum(self.hidden_activation(self.W0,derivative=True))
                self.h_bias = self.h_bias-(self.learning_rate*x_cap)
                self.o_bias = self.o_bias-(self.learning_rate*x_cap)                
                self.layer2 = 0
                self.W0 = []
                self.W2 = []
                self.W3 = []
            count_epoch += 1
            # calculating error loss history values
            ps = softmax(self.WC)
            pr = []
            for probs in ps:
                probs = probs.tolist()
                pr.append(probs.index(max(probs)))
            pr = np.array(pr)
            d = (self._loss_function(y,pr))
            self._loss_history.append(d)
            self.WC = []
            # break condition
            if(0.0 or -0.0 or 0 in self._loss_history):
                break
        self._y = y
        np.random.seed(42)

        # raise NotImplementedError('This function must be implemented by the student.')

    def fit(self, X, y):
        """
        Fits the model to the provided data matrix X and targets y and stores the cross-entropy loss every 20
        iterations.

        Args:
            X: A numpy array of shape (n_samples, n_features) representing the input data.
            y: A numpy array of shape (n_samples,) representing the true class values for each sample in the input data.

        Returns:
            None.
        """
        
        self._initialize(X, y)

    def predict(self, X):
        """
        Predicts class target values for the given test data matrix X using the fitted classifier model.

        Args:
            X: A numpy array of shape (n_samples, n_features) representing the test data.

        Returns:
            A numpy array of shape (n_samples,) representing the predicted target class values for the given test data.
        """

        'Returns the predictions for every element of X'
        
        self.W0 = []
        self.W3 = []
        self.W2 = []
        self.layer2 = 0
        for idx, inputs in enumerate(X):
                for idx1 in range(self.n_hidden):
                    self.layer1 = sum(inputs * self._h_weights[idx1])+self.h_bias
                    self.W0.append(self.layer1)
                for idx2 in range(max(self._y)+1):
                    for id1, j in enumerate(self.W0):
                        self.layer2 += (self.hidden_activation(j)
                                        * self._o_weights[idx2][id1])+self.o_bias
                    self.W2.append(self.layer2)
                    self.layer2 = 0
                self.W3.append(self.W2)
                self.W0 = []
                self.W2 = []
        self.final = []
        x1 = softmax(self.W3) 
        for h1 in x1:
            h1 = h1.tolist()
            self.final.append(h1.index(max(h1))) 
        return self.final

        


        raise NotImplementedError(
            'This function must be implemented by the student.')
