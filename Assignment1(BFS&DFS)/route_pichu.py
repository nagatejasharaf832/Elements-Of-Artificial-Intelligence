#!/usr/local/bin/python3
#
# route_pichu.py : a maze solver
#
# Submitted by : [PUT YOUR NAME AND USERNAME HERE]
#
# Based on skeleton code provided in CSCI B551, Fall 2021.

import sys

from numpy import pi
from numpy.lib.function_base import piecewise
visited=[]

# Parse the map from a given filename
def parse_map(filename):
        with open(filename, "r") as f:
                return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]

def valid_index(pos, n, m):
        return 0 <= pos[0] < n  and 0 <= pos[1] < m

# Find the possible moves from position (row, col)
def moves(map, row, col):
        moves=((row+1,col,"D"), (row-1,col,"U"), (row,col-1,"L"), (row,col+1,"R"))

        # Return only moves that are within the house_map and legal (i.e. go through open space ".")
        return [ move for move in moves if valid_index(move, len(map), len(map[0])) and (map[move[0]][move[1]] in ".@" )]


# Perform search on the map

# This function MUST take a single parameter as input -- the house map --
# and return a tuple of the form (move_count, move_string), where:
# - move_count is the number of moves required to navigate from start to finish, or -1
#    if no such route exists
# - move_string is a string indicating the path, consisting of U, L, R, and D characters
#    (for up, left, right, and down)

def search(house_map):
        pichu_loc=[(row_i,col_i) for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if house_map[row_i][col_i]=="p"][0]
        fringe=[(pichu_loc,0,"")]
        visited=[]
        visited.append(pichu_loc)
        while fringe:
                (curr_move, curr_dist, direction)=fringe.pop()
                for move in moves(house_map,*curr_move):
                        print(move)
                        if(move not in visited):    
                                if house_map[move[0]][move[1]]=="@":
                                        return (curr_dist+1,direction+move[2])  # return a dummy answer
                                else:
                                        visited.append(move)
                                        fringe.append(((move[0],move[1]), curr_dist + 1, direction+move[2]))
                                        # fringe.append(((move[0],move[1]), curr_dist + 1, ""))

# Main Function
if __name__ == "__main__":
        house_map=parse_map(sys.argv[1])
        print("Shhhh... quiet while I navigate!")
        solution = search(house_map)
        print("Here's the solution I found:")
        print(solution[0],solution[1])


