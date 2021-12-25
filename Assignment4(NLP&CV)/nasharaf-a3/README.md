# a3

# Part 1: Parts Of Speech Tagging

### 1) The Formulation of the Problem

- Training the data set
For given sentences in train data we are splitting data into bag of words
For these bag of words we are calculating
word count          -    The number of times a word is repeating in the data set.
word with pos count -    The number of times a word with their pos is repeating in the data set
transition count    -    The number of times a pos is repeating in the data set
emission count      -    Word with pos / length of bag of words
emission probability, transition probability, gibbs probability

- Simplified Algorithm
To discover part of speech for each word in the provided sentence, we have to use a Simplified Bayes Net. To get the probability of (speech|word), we calculated the emission probability of each word for all portions of speech and multiplied it by the prior probability for that component of speech. We took the maximum likelihood value and added it to the result for that particular word. This procedure was effective and yielded a satisfactory result.

- HMM
To discover part of speech for each word in the provided sentence, we have to develop HMM using Viterbi Algorithm. We used memoization to calculate the emission and transition probabilities for all parts of speech at each level, and then appended the most likely parts of speech to a list named best. Finally, we went backwards in time to find the most likely route and returned the POS combination.

- Complex MCMC
To find part of speech for each word in the provided sentence, we have to use Gibbs sampling for the complex bayes net. We trained the data by storing the count of present and previous parts of speech combinations in a tuple as a key for dictionary and count as a value to compute gibbs emission probability. We used this information, as well as transition probabilities, to choose a random POS based on this probability. After 500 iterations, we save the POS counts for each word for all samplings and return the POS with the highest count for each word.
----
                  Simple     HMM Complex it's  late  and   you   said  they'd be    here  by    dawn  ''    .    
0. Ground truth  -133.90 -161.56 -307.06 prt   adv   conj  pron  verb  prt    verb  adv   adp   noun  .     .    
      1. Simple  -133.25 -160.99 -304.84 prt   adj   conj  pron  verb  prt    verb  adv   adp   noun  .     .    
         2. HMM  -133.25 -160.99 -304.84 prt   adj   conj  pron  verb  prt    verb  adv   adp   noun  .     .    
     3. Complex  -133.25 -160.99 -304.84 prt   adj   conj  pron  verb  prt    verb  adv   adp   noun  .     .    

==> So far scored 2000 sentences with 29442 words.
                   Words correct:     Sentences correct: 
   0. Ground truth:      100.00%              100.00%
         1. Simple:       93.95%               47.50%
            2. HMM:       95.75%               58.20%
        3. Complex:       95.74%               58.40%
----

### 2) How the Program Runs
We have first calculated all the counts using Bayes,viterbi and gibbs sampling formulaes
- We are training the data set and storing all the values in self variables
- We are finding pos using simplified algorithm
- We are finding pos using viterbi algorithm
- We are finding pos using gibbs sampling algorithm
In the last step we are calculating posterior probabilites of these algorithms for a given sentence 
 
### 3) Difficulties and Design Decisions
The difficulties we faced in this problem is to find pos using viterbi algorithm where in a particular stage
we were unable to back track and find the which table which suits vi table Hence we referenced So many open 
source links and tried to solve this problem
References:
Canvas Videos
http://www.cs.cmu.edu/~guestrin/Class/10701/slides/hmms-structurelearn.pdf

# Part 2 - Ice Tracking

To begin with, this seemed a very interesting problem of HMM which is tricky. Previously we had seen predicting weather throughout the week, POS tagging by observing some variables and emission probabilities. This problem is definitely a demonstration of how complex-looking real-world problems can be solved using simple concepts like HMM. I’m sure most of us have wondered where is the training data and how do I calculate transition probabilities.

## What do we estimate and what do we know?

Row values (y) along Columns (C1, C2, C3,...., Cn) in the image is my Q1, Q2, Q3...Qn
If columns are my observations, pixel values in each column are my emissions for that column

So, this can be put as,
Find, P(Q1, Q2, Q3….Qn | C1,C2, C3... Cn)
In simpler words, for this column what is the probability that this row is my air-ice/ice-rock boundary given the pixel density?

### Helpful Assumptions/Tips 
> Air-Ice boundary is always above Ice-Rock boundary

> The boundary spans the entire image 

> The boundaries are smooth

> Observe the sharp changes in the pixel values

## The idea behind the solution

#### Simple Bayes 
Look for the maximum (m1) edge density or minimum pixel value, that is my most probable Air-Ice boundary.
The second maximum which is at least 10px below m1 is the most probable Ice-Rock boundary 

#### HMM
The problem can be solved as a graph search problem.
We will have a source - the first column of the image and a sink- the last column of the image.
##### Air-Ice
-   The row with the maximum edge strength will be our starting point, and we try to reach the sink considering emission cost and transition cost. The transition cost here would be the cost involved in moving from row Ri in the current column to R0, R1, R2….Rn in the next column.
 - We try to minimize the cost or look for a maximum cell value in the next column.
- We do this at every column till we reach the sink (the last column)

##### Ice-Rock
- We can use a similar strategy only thing is that our emissions will be a little different.
- For convenience, we can remove the Air-ice boundary and 10px layer from the table so that we can use follow the same steps.


#### HMM with Feedback

We consider human feedback points along the emission probability to make our heuristic more accurate. We observed the boundary estimation can be observed to a good extent when chosen feedback points
We have used the same algorithm for the estimation, tweaking the emission probabilities with the help of feedback points.

### Algorithm / Program flow
Simple

    1. Transpose the edge-strength table, moving along columns is now easy.
    2. Loop through each column, get the maximum edge strength, append it to airice_simple list
    3. Remove a the above found boundary with some margin from the table, by calling our removLayer method
    4. Again loop through each coloumn to get the maximum edge strength in each column, append it to icerock_simple
    5. Plot the points we got

HMM


    1. Modify the transposed table such that each value is between 0-1. We do that by eachStrength/Maximum strength each column
    2. We initialise our first state to a row with the maximum edge strength. say 'm'
    3. We recalculate our table or say decide our next state using following parameters
    4. Calculate and modify each row in the next column using (i) cell value (emission probabilty) say 'v' , (ii) How far is the row from previous estimated boundary say 'd', (iii) feedback point if available 'p' or distance from 'm' say 'Dp'  
    
    i.e cell=  v + (dp/totalColums) - [(v/totalColumns) * d]
    This tells us, 
        (i) farther we move away from the previous boundary value, lesser the probability that the cell is boundary
        (ii) Boundary is aligned with the human feedback points
    
    5. Now get the Air-Ice and Ice-Rock boundaries like we did in simple algorithm.
    
### Challenges
The first thing that seemed challeging was to figure out transition probabilities. Though it was obvious, it was somehow not fitting right in the idea of constructing a viterbi table. When I revisited viterbi videos from the lecture, solving the problem as graph search seemed feasible and straight forward, now the transition probabilites no more the problem. However, I struggled writing my heuristic which has to balance the edge strength over transition.
Changing the way I traverse the 2d array, definitely made code lot easier.

### Sample Output

![alt text](https://github.iu.edu/cs-b551-fa2021/nasharaf-nyeniset-phegde-a3/blob/master/part2/output_images/1.1.png?raw=true)

![alt text](https://github.iu.edu/cs-b551-fa2021/nasharaf-nyeniset-phegde-a3/blob/master/part2/output_images/1.2.png?raw=true)

![alt text](https://github.iu.edu/cs-b551-fa2021/nasharaf-nyeniset-phegde-a3/blob/master/part2/output_images/1.3.png?raw=true)

![alt text](https://github.iu.edu/cs-b551-fa2021/nasharaf-nyeniset-phegde-a3/blob/master/part2/output_images/2.1.png?raw=true)

![alt text](https://github.iu.edu/cs-b551-fa2021/nasharaf-nyeniset-phegde-a3/blob/master/part2/output_images/2.2.png?raw=true)

![alt text](https://github.iu.edu/cs-b551-fa2021/nasharaf-nyeniset-phegde-a3/blob/master/part2/output_images/2.3.png?raw=true)


# Part 3 - Reading Text

I have alway wondered how image processing works, how google lense could scan the text in an image, fancy!! This exercise helped me to get some insight about image processing and the results were actually suprisingly accurate, simple bayes could classify the character in the image with less noise with a good accuracy. I personally enjoyed by knowing how the real time applications work by solving this question. 



## What do we estimate ?

The patterns for each character from the test image are our observed variables. O1,O2,..On
Along the length of the given text, character in each position say Q1,Q2,..Qn are hidden variables. 
Each letter in the image which could be noise, have to be estimated, Q1,Q2,..Qn that are hidden. 
If 2d star list for each character in the image are my observations, then
I have to estimate,
P(Q1, Q2, Q3….Qn | O1,O2,O3,..On)

### What do we know
> We have plenty of data sets to train our classifier.
> We are given train image to get train the character patterns
> Transition probabilities that can be calculated from the training data set
> Emission probabilites can be calculated from test patterns and train patterns 

##  Algorithm / Program flow

##### Simple Bayes 
When solving the question using simple bayes, 
We compare all training letters to the test characters for maximum match. Most matching train character will be the final character we assign for each position in the test letters.


##### HMM
 1. Calculate transition matrix from training data set. This can be done by observing transitions of each character to another in the data set.
 2. Calculate emission matrix using the character match strength.
 3. We calculate viterby table using above parameters.
 4. Apply viterby algorithm to estimate each charcter in the data set.

 # 3) Difficulties and Design Decisions
Unable to figure out the process of finding correct word from image using viterbi algorithm
After a lot of effort and reading online resources we did viterbi using which table and back tracking
Here are the references we followed through out our assignment
References:
Canvas Videos




    

