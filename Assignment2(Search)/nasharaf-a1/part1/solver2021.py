#!/usr/local/bin/python3
# solver2021.py : 2021 Sliding tile puzzle solver
#
# Code by: lfox, nasharaf, lkota
#
# Based on skeleton code by D. Crandall & B551 Staff, September 2021
#

import sys
import numpy as np

ROWS=5
COLS=5

RIGHT = 'R'
LEFT = 'L'
UP = 'U'
DOWN = 'D'
OUTER = 'O'
INNER = 'I'

SOL_BOARD = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15],
          [16, 17, 18, 19, 20], [21, 22, 23, 24, 25]]


def printable_board(board):
    return [ ('%3d ')*COLS  % board[j:(j+COLS)] for j in range(0, ROWS*COLS, COLS) ]


# Heuristic function to eval how good a move is
def heuristic_func(current_board):
    wrong_pos = 0
    manhattan_val = 0
    for i in range(0, ROWS):
        for j in range(0, COLS):
            if current_board[i][j] != SOL_BOARD[i][j]:
                wrong_pos += 1
            position = solution_val_postion(current_board[i][j])
            manhattan_val += abs(i - position[0]) + abs(j - position[1])
    return (manhattan_val + wrong_pos)/8

def solution_val_postion(val):
    for i in range(0, ROWS):
        for j in range(0, COLS):
            if SOL_BOARD[i][j] == val:
                return (i, j)
    return (0, 0)


# return a list of possible successor states
def successors(current_board):
    successors = []
    board_as_list = current_board.board.tolist()
    # Up for each column
    successors.extend(successor_up(board_as_list, current_board.path))
    # Down for each column
    successors.extend(successor_down(board_as_list, current_board.path))
    # Left for each row
    successors.extend(successor_left(board_as_list, current_board.path))
    # Right for each row
    successors.extend(successor_right(board_as_list, current_board.path))
    # Rotate outer clockwise
    successors.append(successor_outer_clockwise(board_as_list, current_board.path))
    # Rotate outer counter-clockwise
    successors.append(succesor_outer_counter_clockwise(board_as_list, current_board.path))
    # Rotate inner clockwise
    successors.append(successor_inner_clockwise(board_as_list, current_board.path))
    # Rotate inner counter-clockwise
    successors.append(successor_inner_counter_clockwise(board_as_list, current_board.path))
    return successors

def successor_outer_clockwise(board, current_path):
    new_board = board.copy()
    new_board = np.array(move_clockwise(new_board))
    new_path = add_to_path(current_path, OUTER + 'c')
    return BoardState(new_board, new_path, heuristic_func(new_board) + len(new_path))

def succesor_outer_counter_clockwise(board, current_path):
    new_board = board.copy()
    new_board = np.array(move_cclockwise(new_board))
    new_path = add_to_path(current_path, OUTER + 'cc')
    return BoardState(new_board, new_path, heuristic_func(new_board) + len(new_path))

def successor_inner_clockwise(board, current_path):
    new_board = board.copy()
    new_board = np.array(move_inner_clockwise(new_board))
    new_path = add_to_path(current_path, INNER + 'c')
    return BoardState(new_board, new_path, heuristic_func(new_board) + len(new_path))

def successor_inner_counter_clockwise(board, current_path):
    new_board = board.copy()
    new_board = np.array(move_inner_counter_clockwise(new_board))
    new_path = add_to_path(current_path, INNER + 'cc')
    return BoardState(new_board, new_path, heuristic_func(new_board) + len(new_path))

def successor_up(board, current_path):
    successors = []

    for i in range(0, COLS):
        new_board = board.copy()
        new_board = transpose_board(new_board)
        new_board = move_left(new_board, i)
        new_board = transpose_board(new_board)
        new_board = np.array(new_board)
        new_path = add_to_path(current_path, UP + str(i+1))
        successors.append(BoardState(new_board, new_path, heuristic_func(new_board) + len(new_path)))
    return successors

def successor_down(board, current_path):
    successors = []
    for i in range(0, COLS):
        new_board = board.copy()
        new_board = transpose_board(new_board)
        new_board = move_right(new_board, i)
        new_board = transpose_board(new_board)
        new_board = np.array(new_board)
        new_path = add_to_path(current_path, DOWN + str(i+1))
        successors.append(BoardState(new_board, new_path, heuristic_func(new_board) + len(new_path)))
    return successors

def successor_left(board, current_path):
    successors = []
    for i in range(0, ROWS):
        new_board = board.copy()
        new_board = move_left(new_board, i)
        new_board = np.array(new_board)
        new_path = add_to_path(current_path, LEFT + str(i+1))
        successors.append(BoardState(new_board, new_path, heuristic_func(new_board) + len(new_path)))
    return successors

def successor_right(board, current_path):
    successors = []
    for i in range(0, ROWS):
        new_board = board.copy()
        new_board= move_right(new_board, i)
        new_board = np.array(new_board)
        new_path = add_to_path(current_path, RIGHT + str(i+1))
        successors.append(BoardState(new_board, new_path, heuristic_func(new_board) + len(new_path)))
    return successors


# check if we've reached the goal
def is_goal(state):
    for i in range(0, ROWS):
        for j in range(0, COLS):
            if state.board[i][j] != SOL_BOARD[i][j]:
                return False
    return True

def solve(initial_board):
    board_arr = np.array(initial_board)
    board_arr = np.reshape(board_arr, (-1, 5))
    fringe = [BoardState(board_arr, [], 0)]
    fringe_dict = {}
    fringe_dict[hash_board(fringe[0].board)] = fringe[0]
    closed = []
    while len(fringe) > 0:
        fringe = sorted(fringe, key=lambda fringe_entry: fringe_entry.heuristic_val, reverse = True)
        curr_board_state = fringe.pop()
        if is_goal(curr_board_state):
            return curr_board_state.path
        # Add closed collection
        old_hash_val = hash_board(curr_board_state.board)
        closed.append(old_hash_val)
        if old_hash_val in fringe_dict:
            del fringe_dict[old_hash_val]
        new_successors = successors(curr_board_state)
        if len(new_successors) > 0:
            for new_board in new_successors:
                hash_val = hash_board(new_board.board)
                if hash_val not in closed:
                    if hash_val in fringe_dict:
                        if not fringe_has_board_with_shorter_sol(new_board, fringe_dict[hash_val]):
                            fringe.remove(fringe_dict[hash_val])
                            fringe.append(new_board)
                            fringe_dict[hash_val] = new_board
                            continue
                    else:
                        fringe.append(new_board)
                        fringe_dict[hash_val] = new_board
    return ["No solution"]

def fringe_has_board_with_shorter_sol(board_state, existing_val):
    if len(existing_val.path) < len(board_state.path):
        return True
    return False

def hash_board(board):
    return hash(str(board.tobytes()))

### From test file
def transpose_board(board):
    """Transpose the board --> change row to column"""
    return [list(col) for col in zip(*board)]


def move_clockwise(board):
    """Move the outer ring clockwise"""
    board[0]=[board[1][0]]+board[0]
    residual=board[0].pop()
    board=transpose_board(board)
    residual=rotate_right(board,-1,residual)
    board=transpose_board(board)
    residual=rotate_left(board,-1,residual)
    board=transpose_board(board)
    residual=rotate_left(board,0,residual)
    board=transpose_board(board)
    return board

def move_inner_clockwise(board):
    board=np.array(board)
    inner_board=board[1:-1,1:-1].tolist()
    inner_board = move_clockwise(inner_board)
    board[1:-1,1:-1]=np.array(inner_board)
    board=board.tolist()
    return board

def move_inner_counter_clockwise(board):
    board=np.array(board)
    inner_board=board[1:-1,1:-1].tolist()
    inner_board = move_cclockwise(inner_board)
    board[1:-1,1:-1]=np.array(inner_board)
    board=board.tolist()
    return board

def move_right(board, row):
    """Move the given row to one position right"""
    board[row] = board[row][-1:] + board[row][:-1]
    return board

def move_left(board, row):
    """Move the given row to one position left"""
    board[row] = board[row][1:] + board[row][:1]
    return board

def rotate_right(board,row,residual):
    board[row] = [board[row][0]] +[residual] + board[row][1:]
    residual=board[row].pop()
    return residual


def rotate_left(board,row,residual):
    board[row] = board[row][:-1] + [residual] + [board[row][-1]]
    residual=board[row].pop(0)
    return residual


def move_clockwise(board):
    """Move the outer ring clockwise"""
    board[0]=[board[1][0]]+board[0]
    residual=board[0].pop()
    board=transpose_board(board)
    residual=rotate_right(board,-1,residual)
    board=transpose_board(board)
    residual=rotate_left(board,-1,residual)
    board=transpose_board(board)
    residual=rotate_left(board,0,residual)
    board=transpose_board(board)
    return board


def move_cclockwise(board):
    """Move the outer ring counter-clockwise"""
    board[0]=board[0]+[board[1][-1]]
    residual=board[0].pop(0)
    board=transpose_board(board)
    residual=rotate_right(board,0,residual)
    board=transpose_board(board)
    residual=rotate_right(board,-1,residual)
    board=transpose_board(board)
    residual=rotate_left(board,-1,residual)
    board=transpose_board(board)
    return board

def add_to_path(current_path, curr_move):
    path = []
    if len(current_path) > 0:
        path.extend(current_path)
    path.append(curr_move)
    return path


class BoardState:
    def __init__(self, board, path, heuristic_val):
        self.board = board
        self.path = path
        self.heuristic_val = heuristic_val

# Please don't modify anything below this line
#
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected a board filename"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [ int(i) for i in line.split() ]

    if len(start_state) != ROWS*COLS:
        raise(Exception("Error: couldn't parse start state file"))

    print("Start state: \n" +"\n".join(printable_board(tuple(start_state))))

    print("Solving...")
    route = solve(tuple(start_state))
    
    print("Solution found in " + str(len(route)) + " moves:" + "\n" + " ".join(route))
