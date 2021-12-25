# Assignment 1
## Team: lfox, nasharaf, lkota

### Part 1 - 2021 Sliding tile puzzle solver:
#### State Space - All valid states of the graph from initial state including rotations and other valid moves.

#### Successor Function - successors function that take a current move and path and returns all valid moves from that particular position.

#### Cost Function - Takes board and evaluates misplaced tiles and Manhattan distance reduced by a factor to improve admissibility

#### Goal State - Manipulate puzzle to goal state in the shortest moves

#### Initial State - Initial puzzle 

###### Improvements
1. Implement hashing and hashmap to considerably reduce the run time.
2. Cleaned up code warnings in my code and existing skeleton code by running pylint add addressing issues.
3. Created class to encapsulate Board State.
###### Questions
1. In this problem, what is the branching factor of the search tree?  All valid moves so 5 rows can move right and left, 5 columns can be moved up and down and the outer and inner rotation can be rotated clockwise and counterclockwise.  The answer is (5*2+5*2+2*2) 24.
2. If  the  solution  can  be  reached  in  7  moves,  about  how  many  states  would  we  need  to  explore  before  wefound it if we used BFS instead of A* search?  The answer is O(b^d) so 24^7 = 4,586,471,424.  So greater than that many states approximately.

### Part 2 Road Trip:
#### State Space - all the highway segments of North America

#### Successor Function - all the routes from start city in road segments data

#### Cost Function - number of segments/distance travelled/time taken/delivery hours

#### Goal State - end city

#### Initial State - start city

###### Improvements - 
1. We have used priority queue for pop inside array which have least a*value
2. using a*value we are deciding which successor to move on in the next step
3. With given cost + a*value we can move the successor into fringe.

### Part 3 Choosing teams:
#### State Space - Any valid configuration assigning students to 1 to many teams.

#### Cost Function - calculate_cost takes in an assignment configuration and the preference object and calculates based on rules in assignment.

#### Goal State - The minimum cost team that makes the represents satisfying the problem space.

#### Initial State - Assign everyone to working alone.

#### Implementation - Takes list of students and randomly assigns groupings based on random group sizes and configurations.  Cost is evaluated and any new best group is replaced.

###### Improvements
1. Add hashing of assignment teams to never bother calculating cost or considering duplicates.
2. Create multiple classes to clearly identify preferces Assignment teams and the total group.
3. Cleaned up code warnings in my code and existing skeleton code by running pylint add addressing issues.