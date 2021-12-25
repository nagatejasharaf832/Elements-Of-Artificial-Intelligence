
Route pichus:
------------
Initial state:
The initial state in route pichus is a printable map with walls(X) and having NxM cells 
which consists of one pichu in any of the square box and @ A.K.A human in another square box
Goal state:
The goal state is to return the shortest path from pichu location to @ location and the shortest
distance pichu has traveled to reach the goal state
successor function:
The successor function is that for any location of pichu lets say (r,c)
it has 4 different directions it can reach the next possible state
(r+1,c),(r-1,c)(r,c+1),(r,c-1) i.e Up,Down,Left and Right
cost function:
The cost function is same all over the map where if pichu travels in any one of the above
directions it will be costed as 1.
search method:
The search method used to find shortest path is BFS
In this problem actually the initial code is already written what I did is just added and printed the 
directions where pichu is supposed to go and also added the visited locations where it should not go again
which has been stored in an array.
_____________________________________________
Arrange pichus:
--------------
Initial state:
The initial state for arrange pichus is a map with no or a limited number of pichus and consists of walls 
indicated as (X)
Goal state:
The goal is that with given input which is map and number of pichus (k)
we need to arrange k pichus in the given map where no two pichus should see each other and if there is a 
wall then pichu can be placed so that in between two pichus there is a wall so that they cant see each other
in addition to that pichu can also be places near @ indication.
successor function:
The successor function is that while arranging pichus we have to make sure that 
the point of location is not been attacked by any other pichu which is already placed in the previous location
if the point is under attack then it should either search for a new point and it should back track
and visit the next possible point or it should re arrange the previous pichu.
If there is no solution it will return False.
cost function:
The cost function will depend on the successor function where which logic is pichu been applied to 
fastly arrange its location in the map by searching check point function.
search method:
In this problem DFS has been implementd as it goes in depth and back track if the arrangement wont work.
The initial code in this problem is written such that it back tracks if a solution is not found
So what I did is just added all the conditions or point where pichu is not allowed to arrange in which
it checks the attacking point in an array if its present location is not matching with that array
then it can be positioned in that particular point and so on..
