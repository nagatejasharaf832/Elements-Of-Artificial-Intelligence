# a4

# Part 1: KNN Neighbours

### 1) The Formulation of the Problem

The closest neighbor calculation works by registering a network standard on the test and train information's vector contrast. This grid standard assists us in calculating a comparable euclidean distance between test and train data. Now based on all the distances sort them and find the nearest distance in the array after that
We will slice the array based on n neighbours once the slice happens we can map these indexes to classes 
Now finally do mode which means which class is repeating more time need to be appened to final array
now return this final array and chart results in knn digits and knn iris

### 2) How the Program Runs
I have first calculated all the distances from test to train data features
- I am  adding a condition where if weights is distance or not if yes 1/e1 else infinity
- I am  appending all distances and classes
- Sort all the distances to find shortest distance
- slice this array based on neighbours and calcuating classes
 
### 3) Difficulties and Design Decisions
While doing this problem I faced a difficulty on how to find distance between train data and test data
and sort data correctly

# Part 2: Multilayer perceptron 

### 1) The Formulation of the Problem
Multilayer perceptron is also known as Feed Farword Artificial neural network and it uses a supervised learning technique which is know as back propogation.
Steps I followed:
- activation functions in utils.py
- Initialize weights
- feed farward propogation
- error derviation
- backword propogation
- update weights
### 2) How the Program Runs
- I have first calculated all weights based on random values 
- initializing weights based on random values
- using np.dot or direct matrix multiplication calculating feed forward propogation values into W0 and W2
- appending all output values in the output layer into W3 
- calculating error for these output values target - softmax(output values)
- backpropogate layers and update weights based on formule - w5 = w5-learningrate*error* activation gradient descent way
- iterate the whole process until loss histroy becomes zero or full number of iterations finished
### 3) Difficulties and Design Decisions
I faced a difficulty in back propogation where I was unable to update weights gradiently and took so much time which researching about formulaes

References
Canvas Videos
https://machinelearningmastery.com/implement-backpropagation-algorithm-scratch-python/
https://machinelearningmastery.com/cross-entropy-for-machine-learning/






    

