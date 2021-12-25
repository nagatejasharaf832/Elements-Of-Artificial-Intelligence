# Simple quintris program! v0.2
# D. Crandall, Sept 2021
# NagathejaSharaf aka nasharaf
# - with sathup & holtjohn 

from AnimatedQuintris import *
from SimpleQuintris import *
from kbinput import *
import time, sys
from copy import deepcopy, copy

class HumanPlayer:
    def get_moves(self, quintris):
        print("Type a sequence of moves using: \n  b for move left \n  m for move right \n  n for rotation\n  h for horizontal flip\nThen press enter. E.g.: bbbnn\n")
        moves = input()
        return moves

    def control_game(self, quintris):
        while 1:
            c = get_char_keyboard()
            commands =  { "b": quintris.left, "h": quintris.hflip, "n": quintris.rotate, "m": quintris.right, " ": quintris.down }
            commands[c]()

#####
# This is the part you'll want to modify!
# Replace our super simple algorithm with something better
#
class ComputerPlayer:
    # This function should generate a series of commands to move the piece into the "optimal"
    # position. The commands are a string of letters, where b and m represent left and right, respectively,
    # and n rotates. quintris is an object that lets you inspect the board, e.g.:
    #   - quintris.col, quintris.row have the current column and row of the upper-left corner of the 
    #     falling piece
    #   - quintris.get_piece() is the current piece, quintris.get_next_piece() is the next piece after that
    #   - quintris.left(), quintris.right(), quintris.down(), and quintris.rotate() can be called to actually
    #     issue game commands
    #   - quintris.get_board() returns the current state of the board, as a list of strings.
    #

    # def genetic(self):
        
 
    # objective function
    # def objective(self,x):
    #     return x[0]**2.0 + x[1]**2.0
    
    # # decode bitstring to numbers
    # def decode(self,bounds, n_bits, bitstring):
    #     decoded = list()
    #     largest = 2**n_bits
    #     for i in range(len(bounds)):
    #         # extract the substring
    #         start, end = i * n_bits, (i * n_bits)+n_bits
    #         substring = bitstring[start:end]
    #         # convert bitstring to a string of chars
    #         chars = ''.join([str(s) for s in substring])
    #         # convert string to integer
    #         integer = int(chars, 2)
    #         # scale integer to desired range
    #         value = bounds[i][0] + (integer/largest) * (bounds[i][1] - bounds[i][0])
    #         # store
    #         decoded.append(value)
    #     return decoded
    
    # # tournament selection
    # def selection(self,pop, scores, k=3):
    #     # first random selection
    #     selection_ix = randint(len(pop))
    #     for ix in randint(0, len(pop), k-1):
    #         # check if better (e.g. perform a tournament)
    #         if scores[ix] < scores[selection_ix]:
    #             selection_ix = ix
    #     return pop[selection_ix]
    
    # # crossover two parents to create two children
    # def crossover(self,p1, p2, r_cross):
    #     # children are copies of parents by default
    #     c1, c2 = p1.copy(), p2.copy()
    #     # check for recombination
    #     if rand() < r_cross:
    #         # select crossover point that is not on the end of the string
    #         pt = randint(1, len(p1)-2)
    #         # perform crossover
    #         c1 = p1[:pt] + p2[pt:]
    #         c2 = p2[:pt] + p1[pt:]
    #     return [c1, c2]
    
    # # mutation operator
    # def mutation(self,bitstring, r_mut):
    #     for i in range(len(bitstring)):
    #         # check for a mutation
    #         if rand() < r_mut:
    #             # flip the bit
    #             bitstring[i] = 1 - bitstring[i]
    
    # genetic algorithm
    # def genetic_algorithm(self,objective, bounds, n_bits, n_iter, n_pop, r_cross, r_mut):
    #     # initial population of random bitstring
    #     pop = [randint(0, 2, n_bits*len(bounds)).tolist() for _ in range(n_pop)]
    #     # keep track of best solution
    #     best, best_eval = 0, self.objective(self.decode(bounds, n_bits, pop[0]))
    #     # enumerate generations
    #     for gen in range(n_iter):
    #         # decode population
    #         decoded = [self.decode(bounds, n_bits, p) for p in pop]
    #         # evaluate all candidates in the population
    #         scores = [objective(d) for d in decoded]
    #         # check for new best solution
    #         for i in range(n_pop):
    #             if scores[i] < best_eval:
    #                 best, best_eval = pop[i], scores[i]
    #                 # print(">%d, new best f(%s) = %f" % (gen,  decoded[i], scores[i]))
    #         # select parents
    #         selected = [self.selection(pop, scores) for _ in range(n_pop)]
    #         # create the next generation
    #         children = list()
    #         for i in range(0, n_pop, 2):
    #             # get selected parents in pairs
    #             p1, p2 = selected[i], selected[i+1]
    #             # crossover and mutation
    #             for c in self.crossover(p1, p2, r_cross):
    #                 # mutation
    #                 self.mutation(c, r_mut)
    #                 # store for next generation
    #                 children.append(c)
    #         # replace population
    #         pop = children
    #     return [best, best_eval]
 

# get the current height of the board
    def get_height(self,area):
        peaks = []
        c = 0
        for col in (area):
            if "x" in col:
                c = c+1
        return c

#get number of holes in the board 
    def get_holes(self,area):
        c = 0
        for col in area:
            for idx,col1 in enumerate(col):
                if(col1 == "x"):
                    c = c+abs((25-idx-(col.count("x"))))
                    break
        return c

#get number of lines cleared after placing the piece
    def get_cleared_lines(self,x):
        c = 0
        return x.get_score

# get the count of number of rows been filled by "x"
    def rows_filled(self,area):
        c = 0
        c1 = []
        for col in area:
                c=c+col.count("x")
                c1.append(c)
                c=0
        return max(c1)

# get how many empty columns are left in the board
    def get_pits(self,area):
        c = 0
        for col in area:
            if(col[0].count("0")==len(area)):
                c=c+col.count("0")
        return (c)

# get absolute difference between heights of columns in the board
    def get_bumpiness(self,area):
        c = 0
        for idx,col in enumerate(area):
                if(idx<len(area)-1):
                    c=c+(abs(area[idx][0].count("x")-area[idx+1][0].count("x")))
        return (c)

# get the number of row transitions in the board
    def get_row_transitions(self,area):
        row_trans = 0
        for x in area:
            res = list(x.replace(" ","0"))
            for idx,n in enumerate(res):
                if n == "x":
                    if(idx!=0):
                        if(res[idx-1]=="0"):
                            row_trans = row_trans+1
                    if(idx+1!=len(res)):
                        if(res[idx+1]=="0"):
                            row_trans = row_trans+1
        return(row_trans)

# get the number of column transitions in the board
    def get_col_transitions(self,area):
        b4 = []
        b5 = []
        b3 = area
        for idx,i in enumerate(b3):
            c = 0
            i = list(i.replace(" ","0"))
            while(c<len(i)):
                b4.append(i[c])
                for j in range(idx+1,len(b3)):
                    j1 = list(b3[j].replace(" ","0"))
                    b4.append(j1[c])
                    if(len(b4)==len(b3)):
                        b5.append(b4)
                        b4 = []
                c=c+1
            break
        b6 = deepcopy(b5)
        pits = self.get_pits(b6)
        bum = self.get_bumpiness(b6)
        holes = self.get_holes(b6)
        col_trans = 0
        for res in b5:
            for idx,n in enumerate(res):
                    if n == "x":
                        if(idx!=0):
                            if(res[idx-1]=="0"):
                                col_trans = col_trans+1
                        if(idx+1!=len(res)):
                            if(res[idx+1]=="0"):
                                col_trans = col_trans+1
        return(col_trans,pits,bum,holes)
                    

# get heuristic values for the current move
    def get_heuristic(self,height,holes,lines,row_trans,col_trans,pits,bum,rows):
        # h = -1.9*float(height)+-0.9*float(holes)+0.9*float(lines)+0.9*float(rows)+-0.5*float(row_trans)+-0.9*float(col_trans)+-0.94*float(pits)+-0.54*float(bum)
        h = -0.510066*float(height)+-1.82663*float(holes)+0.980666*float(lines)+1.7*float(rows)+-0.5*float(row_trans)+-0.9*float(col_trans)+-0.94*float(pits)+-0.384483*float(bum)
        return(h)

# get all successors or moves of the current piece 
    def get_possible_moves(self,quintris1,moves,rot):

        col_co = deepcopy(quintris1)
        col = col_co.col
        pi = col_co.get_piece()
        piece = len(max(pi[0],key = len))
        col1 = 15-col-piece
        height1 = self.get_height(quintris1.get_board())
        lines = 0
        x = {}
        # move the quintris to deep left and iterate it from that position to col
        while(col):
            temp_q = deepcopy(quintris1)
            # move quintris to atmost left position
            for i in range(col):
                temp_q.left()
            
            temp_area = temp_q.down()
            height2 =  self.get_height(temp_q.get_board())
            
            if(height2<height1):
                lines = lines+(abs(height2-height1))

            hei = self.get_height(temp_q.get_board())
            row_trans = self.get_row_transitions(temp_q.get_board())
            col_trans,pits,bum,holes = self.get_col_transitions(temp_q.get_board())
            rows_filled = self.rows_filled(temp_q.get_board())
            heu = self.get_heuristic(hei,holes,lines,row_trans,col_trans,pits,bum,rows_filled)
            
            # store all the values into a dict for reference
            x["state"] = temp_q.get_board()
            x["height"] = hei
            x["holes"] = holes
            x["lines_clr"] = lines
            x["row_trans"] = row_trans
            x["col_trans"] = col_trans
            x["pits"] = pits
            x["bump"] = bum
            x["rows"] = rows_filled
            x["heu"] = heu
            st = "b"*col
            x["move"] = rot+str(st)
            
            moves.append(x)
            x = {}
            col = col-1
        # move the quintris to deep right and iterate it from that position to col
        while(col1):
            temp_q = deepcopy(quintris1)

            for i in range(col1):
                temp_q.right()
            
            temp_area = temp_q.down()
            height2 =  self.get_height(temp_q.get_board())
            
            if(height2<height1):
                lines = lines+(abs(height2-height1))
            
            hei = self.get_height(temp_q.get_board())
            row_trans = self.get_row_transitions(temp_q.get_board())
            col_trans,pits,bum,holes = self.get_col_transitions(temp_q.get_board())
            rows_filled = self.rows_filled(temp_q.get_board())
            heu = self.get_heuristic(hei,holes,lines,row_trans,col_trans,pits,bum,rows_filled)
            
            x["state"] = temp_q.get_board()
            x["height"] = hei
            x["holes"] = holes
            x["lines_clr"] = lines
            x["row_trans"] = row_trans
            x["col_trans"] = col_trans
            x["pits"] = pits
            x["bump"] = bum
            x["rows"] = rows_filled
            x["heu"] = heu
            st = "m"*col1
            x["move"] = rot+str(st)
            
            moves.append(x)
            x = {}
            col1=col1-1
        
        return moves

# get best move using greedy heuristic among all moves
    def get_best_move(self,moves):
        # initialize mini to negative infinity
        mini = -1000000000000000000000000000000000000000
        best_moves = []
        idxx = 0
        # check move with greater heuristic value
        for idx,move in enumerate(moves):
            if(move["heu"]>mini):
                mini = move["heu"]
                idxx = idx
        best_moves.append((moves[idxx]))
        return best_moves

# Given a new piece (encoded as a list of strings) and a board (also list of strings), 
# this function should generate a series of commands to move the piece into the "optimal"
# position. The commands are a string of letters, where b and m represent left and right, respectively,
# and n rotates. 
#
# computer simple function which will return the string of moves to perform
    def get_moves(self, quintris):

        area = quintris.get_board()
        # copy original quintris 
        temmp_quintris = deepcopy(quintris)

        i=4 #rotations
        j=2 #hflips
        moves = []
        rot = ""
        # calculate flips and rotations and send the quintris to get all successors or moves
        while(i+j):
            if(j<2 and j!=0 and j>0):
                rot = rot+"h"*abs(j-2)
                temmp_quintris.hflip()
            if(i<4 and i!=0 and i>0):
                rot = rot+"n"*abs(i-4)
                temmp_quintris.rotate()
            moves = self.get_possible_moves(temmp_quintris,moves,rot)
            j= j-1
            if(j==0):
                i=i-1
        # get best move 
        peaks = self.get_best_move(moves)
        return str(peaks[0]["move"])
       
    # This is the version that's used by the animted version. This is really similar to get_moves,
    # except that it runs as a separate thread and you should access various methods and data in
    # the "quintris" object to control the movement. In particular:
    #   - quintris.col, quintris.row have the current column and row of the upper-left corner of the 
    #     falling piece
    #   - quintris.get_piece() is the current piece, quintris.get_next_piece() is the next piece after that
    #   - quintris.left(), quintris.right(), quintris.down(), and quintris.rotate() can be called to actually
    #     issue game commands
    #   - quintris.get_board() returns the current state of the board, as a list of strings.
    #
    def control_game(self, quintris):
        # another super simple algorithm: just move piece to the least-full column
        while 1:
            # time.sleep(0.1)
            x = self.get_moves(quintris)
            x = list(x)
            for i in x:
                if(i=="b"):
                    quintris.left()
                elif(i=="m"):
                    quintris.right()
                elif(i=="n"):
                    quintris.rotate()
            time.sleep(2)
            quintris.down()

###################
#### main program

(player_opt, interface_opt) = sys.argv[1:3]

try:
    if player_opt == "human":
        player = HumanPlayer()
    elif player_opt == "computer":
        player = ComputerPlayer()
    else:
        print("unknown player!")

    if interface_opt == "simple":
        quintris = SimpleQuintris()
    elif interface_opt == "animated":
        quintris = AnimatedQuintris()
    else:
        print("unknown interface!")

    quintris.start_game(player)

except EndOfGame as s:
    print("\n\n\n", s)



