#!/usr/local/bin/python3
#
# arrange_pichus.py : arrange agents on a grid, avoiding conflicts
#
# Submitted by : [PUT YOUR NAME AND USERNAME HERE]
#
# Based on skeleton code in CSCI B551, Fall 2021.

# class Target:


import sys

from numpy import pi

target = 0
points = []
np=0
result=[]

def pos_x(house_map,pich_loc):
    print("posss",printable_house_map(house_map))
    global points
    points=[]
    points = set(points)
    # for Upword
    for low in pich_loc:
        while(low[0]>0):
            low = (low[0]-1,low[1])
            if(house_map[low[0]][low[1]] in "@X"):
                   break;
            else:
                points.update({low})
                # points = list(points)
                # points.append(low)
                # points = list(set(points))
    
        # for Downword
    for low in pich_loc:
        while(low[0]<(len(house_map)-1)):
            low = (low[0]+1,low[1])
            if(house_map[low[0]][low[1]] in "@X"):
                  break;
            else:
                points.update({low})
                # points.append(low)
                # points = list(set(points))
    
        # for Left
    for low in pich_loc:
        while(low[1]>0):
            low = (low[0],low[1]-1)
            if((house_map[low[0]][low[1]]) in "@X"):
                  break;
            else:
                points.update({low})
                # points = list(set(points))
    
        # for right
    for low in pich_loc:
        while(low[1]<(len(house_map[0])-1)):
            low = (low[0],low[1]+1)
            if((house_map[low[0]][low[1]]) in "@X"):
                  break;
            else:
                points.update({low})
                # points = list(set(points))
    
    # for top slash diagnol
    for low in pich_loc:
        while(house_map[low[0]][low[1]] and low[0]>0 and low[1]<(len(house_map[0])-1)):
            low = (low[0]-1,low[1])
            low = (low[0],low[1]+1)
            
            if((house_map[low[0]][low[1]]) in "@X"):
                  break;
            else:
                points.update({low})
                # points = list(set(points))
        # for bottom slash diagnol
    for low in pich_loc:
        while(house_map[low[0]][low[1]] and (low[0]<(len(house_map)-1)) and low[1]>0):
            low = (low[0]+1,low[1])
            low = (low[0],low[1]-1)
            if((house_map[low[0]][low[1]]) in "@X"):
                  break;
            else:
                points.update({low})
                # points = list(set(points))
                
        # for top back slash diagnol
    for low in pich_loc:
        while(house_map[low[0]][low[1]] and low[0]>0 and low[1]>0):
            low = (low[0]-1,low[1])
            low = (low[0],low[1]-1)
            if((house_map[low[0]][low[1]]) in "@X"):
                  break;
            else:
                points.update({low})
                # points = list(set(points))
                
    
        # for bottom back slash diagnol
    for low in pich_loc:
       while(house_map[low[0]][low[1]] and (low[0]<(len(house_map)-1)) and low[1]<(len(house_map[0])-1)):
            low = (low[0]+1,low[1])
            low = (low[0],low[1]+1)
            if((house_map[low[0]][low[1]]) in "@X"):
                  break;
            else:
                points.update({low})
                # points = list(set(points))
    points = (list(set(points)))
    # print(points)
    return points      

def check_point(t):
    # if(t==(2,3)):
    #     print(t,points)
    # print("----p>>>",points)
    if t not in points:
        return True
    else:
        # print("-false---p>>>",t,list(set(points)))
        return False
def is_goal(house_map, k):
    return count_pichus(house_map) == k 
# Parse the map from a given filename
def parse_map(filename):
	with open(filename, "r") as f:
		return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]

# Count total # of pichus on house_map
def count_pichus(house_map):
    return sum([ row.count('p') for row in house_map ] )

# Return a string with the house_map rendered in a human-pichuly format
def printable_house_map(house_map):
    return "\n".join(["".join(row) for row in house_map])

# Add a pichu to the house_map at the given position, and return a new house_map (doesn't change original)
def add_pichu(house_map, row, col):
    # print("--->>",(row,col),"--->>p",points)
    return house_map[0:row] + [house_map[row][0:col] + ['p',] + house_map[row][col+1:]] + house_map[row+1:] 

# Get list of successors of given house_map state
def successors(house_map):
    # print(points)
    pichu_loc=[(row_i,col_i) for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if house_map[row_i][col_i]=="p"]
    loc = pos_x(house_map,pichu_loc)
    return [add_pichu(house_map, r, c) for r in range(0, len(house_map)) for c in range(0,len(house_map[0])) if check_point((r,c)) and house_map[r][c] == '.']

def solve(initial_house_map,k):
    pichu_loc=[(row_i,col_i) for col_i in range(len(initial_house_map[0])) for row_i in range(len(initial_house_map)) if initial_house_map[row_i][col_i]=="p"]
    loc = pos_x(initial_house_map,pichu_loc)
    fringe = [initial_house_map]
    while len(fringe) > 0:
            # print("--fringe--",printable_house_map(fringe[0]))
            for new_house_map in successors( fringe.pop() ):
                if is_goal(new_house_map,k):
                    return(new_house_map,True)
                fringe.append(new_house_map)
    return ("",False)
# check if house_map is a goal state
# def is_goal(house_map):
    
#     return count_pichus(house_map) == np 

# Arrange agents on the map
#
# This function MUST take two parameters as input -- the house map and the value k --
# and return a tuple of the form (new_house_map, success), where:
# - new_house_map is a new version of the map with k agents,
# - success is True if a solution was found, and False otherwise.
#
# global target 

# def solve(initial_house_map,k):
#     return solves(initial_house_map,0,0)

# def checkPichu(house_map, row,col):
#     if row>=len(house_map) or col>=len(house_map[0]) or house_map[row][col] in "p@X":
#         return False
#     pichu_loc=[(row_i,col_i) for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if house_map[row_i][col_i]=="p"]
#     pos_x(house_map,pichu_loc)
#     return (check_point((row,col)))


# def solves(house_map,row,col):
#     global result
#     if(is_goal(house_map)):
#         print(printable_house_map(house_map))
#         return True

    # if(row>=len(house_map)):
    #     return False
    
    # print(row,col)

    # res=False
    # temp=col
    # for i in range(row,len(house_map)):
    #     print(i,col,"ds")
    #     if len(house_map)>0 and col==len(house_map[0]):
    #         col=0
    #     if(checkPichu(house_map,i,col)):
    #         house_map[i][col]='p'
    #         res=solves(house_map,i,col+1) or res
    #         house_map[i][col]='.'
    # if(col == temp):
    #     res=solves(house_map,row,col+1) or res


    # return res





# Main Function
if __name__ == "__main__":

    house_map=parse_map(sys.argv[1])
    # print(target)
    
    k = int(sys.argv[2])
    # np=k
    print ("Starting from initial house map:\n" + printable_house_map(house_map) + "\n\nLooking for solution...\n")
    solution = solve(house_map,k)
    print ("Here's what we found:",solution)
    print (printable_house_map(solution[0]) if solution[1] else "False")


