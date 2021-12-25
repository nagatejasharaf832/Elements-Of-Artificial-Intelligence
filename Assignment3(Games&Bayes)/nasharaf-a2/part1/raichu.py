# raichu.py : Play the game of Raichu
#
# John Holt aka holtjohn
# - with sathup & nasharaf 
#
# Based on skeleton code by D. Crandall, Oct 2021
#
import sys
import time

# Converts to easy-to-view grid
def board_to_string(board, N):
    return "\n".join(board[i:i+N] for i in range(0, len(board), N))

# Returns the index in board string given a (row, column) coordinate pair
def coord_index(coord, N):
    row,col = coord
    index = row*N+col
    return index

# Updates board to a new board to reflect move made
def move_to_board(move,board,N):
    # Accounts for no-moves boards
    if move == [0]:
        return board
    # All other boards
    piece = board[move[1][0]*N+move[1][1]]
    initial_board = board[:move[1][0]*N+move[1][1]]+'.'+board[move[1][0]*N+move[1][1]+1:]
    initial_board = initial_board[:move[2][0]*N+move[2][1]]+piece+initial_board[move[2][0]*N+move[2][1]+1:]
    if move[3]!=[]:
        initial_board = initial_board[:move[3][0][0]*N+move[3][0][1]]+'.'+initial_board[move[3][0][0]*N+move[3][0][1]+1:]
    for i in range(N):
        if initial_board[i] == 'b' or initial_board[i] == 'B':
            initial_board = initial_board[:i]+'$'+initial_board[i+1:]
    for i in range(N**2-N,N**2):
        if initial_board[i] == 'w' or initial_board[i] == 'W':
            initial_board = initial_board[:i]+'@'+initial_board[i+1:]
    return initial_board

# Whenever a move would take a piece, this function determines if that is the
# last enemy piece
def game_over(board,player):
    if player == 'w':
        enemy = ['b','B','$']
    else:
        enemy = ['w','W','@']
    pieces = 0
    for char in board:
        if char in enemy:
            pieces+=1
    if pieces == 1:
        return True
    else:
        return False

# Creates all legal moves for all pieces, along with the following move scores:
# Note: Max scores are positive, Min scores are negative. Expected score
#       differential represents true expected value of a move.
#   MOVEMENT POINTS
#   - If no Raichus exist on your team, forward progress earns a percentage
#     of 3 points for Pikachus and 2 points for Pichus, based on how many rows
#     the move advances the piece.
#   - If at least one Raichu exists in your team, forward progress scoring is
#     turned off. Reactivates when opponent has a Raichu.
#   - Raichu moves earn points equal to (number of pieces enemy owns less 1)
#     divided by 3.
#   JUMPING POINTS
#   - Jumping a Pichu is worth 6 points (stacks with movement points)
#   - Jumping a Pikachu is worth 8 points (stacks with movement points)
#   - Jumping a Raichu is worth 10 points (stacks with movement points)
#   - Jumping the last piece is worth an additional 200 points (ending game)
def all_moves(depth, value, board, N, player):
    if player == 'w':
        key = [1,'w','W','@']
        key2 = ['b','B','$']
    if player == 'b':
        key = [-1,'b','B','$']
        key2 = ['w','W','@']
    all_moves = []
    raichu_count = 0
    enemy_strength = 0
    for char in board:
        if char == key[3]:
            raichu_count+=1
        if char == key2[2]:
            raichu_count-=10
        if char in key2:
            enemy_strength+=1
    enemy_strength = (enemy_strength-1)/3+1
    if raichu_count > 0:
        pp_mod = 0
    else:
        pp_mod = 1
    if depth%2 == 0:
        value_mod = 1
    elif depth%2 == 1:
        value_mod = -1
    for j in range(len(board)):
        if board[j] in key:
            coord = (j//N,j%N)
            # Pichu behavior
            if board[j] == key[1]:
                jumped_mod = 0
                new_coord = (coord[0]+key[0],coord[1]+1)
                if new_coord[1]<N and board[coord_index(new_coord,N)] == '.':
                    all_moves.append([value+value_mod*(pp_mod*2/((key[0]+1)/2*(N-1)-key[0]*coord[0])),coord,new_coord,[]])
                elif new_coord[1]<N-1 and new_coord[0]<N-1 and new_coord[0]>0 and board[coord_index(new_coord,N)] == key2[0]:
                    next_coord = (new_coord[0]+key[0],new_coord[1]+1)
                    if board[coord_index(next_coord,N)] == '.':
                        if game_over(board,player):
                            jumped_mod+=200                        
                        all_moves.append([value+value_mod*((pp_mod*2/((key[0]+1)/2*(N-1)-key[0]*coord[0]))*2+6+jumped_mod),coord,next_coord,[new_coord]])
                jumped_mod = 0
                new_coord = (coord[0]+key[0],coord[1]-1)
                if new_coord[1]>-1 and board[coord_index(new_coord,N)] == '.':
                    all_moves.append([value+value_mod*(pp_mod*2/((key[0]+1)/2*(N-1)-key[0]*coord[0])),coord,new_coord,[]])
                elif new_coord[1]>0 and new_coord[0]<N-1 and new_coord[0]>0 and board[coord_index(new_coord,N)] == key2[0]:
                    next_coord = (new_coord[0]+key[0],new_coord[1]-1)
                    if board[coord_index(next_coord,N)] == '.':
                        if game_over(board,player):
                            jumped_mod+=200                         
                        all_moves.append([value+value_mod*((pp_mod*2/((key[0]+1)/2*(N-1)-key[0]*coord[0]))*2+6+jumped_mod),coord,next_coord,[new_coord]])
            # Pikachu behavior
            if board[j] == key[2]:
                # forward motion
                i=1
                jumps = 0
                jumped_mod = 0
                jumped_coord = []
                if (coord[1]==0 or coord[1]==N-1) and (coord[0]==1 or coord[0]==N-2):
                    jumped_mod+=1
                while i <= 3:
                    new_coord = (coord[0]+i*key[0],coord[1])
                    if new_coord[0]>-1 and new_coord[0]<N and board[coord_index(new_coord,N)] == '.':
                        all_moves.append([value+value_mod*(pp_mod*3/((key[0]+1)/2*(N-1)-key[0]*coord[0])*i+jumped_mod),coord,new_coord,jumped_coord])
                        if i == 2 and jumps == 0:
                            break
                        i+=1
                    elif new_coord[0]>0 and new_coord[0]<N-1 and board[coord_index(new_coord,N)] in [key2[0],key2[1]]:
                        next_coord = (new_coord[0]+key[0],new_coord[1])
                        if board[coord_index(next_coord,N)] == '.' and jumps == 0:
                            i+=1
                            jumps+=1
                            jumped_mod = key2.index(board[coord_index(new_coord,N)])*2+6
                            if game_over(board,player):
                                jumped_mod+=200
                            jumped_coord = [new_coord]
                        else:
                            break
                    else:
                        break
                # right motion               
                i=1
                jumps = 0
                jumped_mod = 0
                jumped_coord = []
                while i <= 3:
                    new_coord = (coord[0],coord[1]+i)
                    if new_coord[1]<N and board[coord_index(new_coord,N)] == '.':
                        all_moves.append([value+value_mod*(pp_mod*(0)*i+jumped_mod),coord,new_coord,jumped_coord])
                        if i == 2 and jumps == 0:
                            break
                        i+=1
                    elif new_coord[1]<N-1 and board[coord_index(new_coord,N)] in [key2[0],key2[1]]:
                        next_coord = (new_coord[0],new_coord[1]+i)
                        if board[coord_index(next_coord,N)] == '.' and jumps == 0:
                            i+=1
                            jumps+=1
                            jumped_mod = key2.index(board[coord_index(new_coord,N)])*2+6
                            if game_over(board,player):
                                jumped_mod+=200
                            jumped_coord = [new_coord]
                        else:
                            break
                    else:
                        break                
                # left motion               
                i=1
                jumps = 0
                jumped_mod = 0
                jumped_coord = []
                while i <= 3:
                    new_coord = (coord[0],coord[1]-i)
                    if new_coord[1]>-1 and board[coord_index(new_coord,N)] == '.':
                        all_moves.append([value+value_mod*(pp_mod*(0)*i+jumped_mod),coord,new_coord,jumped_coord])
                        if i == 2 and jumps == 0:
                            break
                        i+=1
                    elif new_coord[1]>0 and board[coord_index(new_coord,N)] in [key2[0],key2[1]]:
                        next_coord = (new_coord[0],new_coord[1]-i)
                        if board[coord_index(next_coord,N)] == '.' and jumps == 0:
                            i+=1
                            jumps+=1
                            jumped_mod = key2.index(board[coord_index(new_coord,N)])*2+6
                            if game_over(board,player):
                                jumped_mod+=200
                            jumped_coord = [new_coord]
                        else:
                            break
                    else:
                        break    
            # Raichu behavior
            if board[j] == key[3]:
                # forward motion
                i = 1
                jumps = 0
                jumped_mod = 0
                jumped_coord = []
                while i < N:
                    new_coord = (coord[0]+i*key[0],coord[1])
                    if new_coord[0]>-1 and new_coord[0]<N and board[coord_index(new_coord,N)] == '.':
                        all_moves.append([value+value_mod*(enemy_strength-1+jumped_mod),coord,new_coord,jumped_coord])
                        i+=1
                    elif new_coord[0]>0 and new_coord[0]<N-1 and board[coord_index(new_coord,N)] in key2:
                        next_coord = (new_coord[0]+key[0],new_coord[1])
                        if board[coord_index(next_coord,N)] == '.' and jumps == 0:
                            i+=1
                            jumps+=1
                            jumped_mod = key2.index(board[coord_index(new_coord,N)])*2+6
                            if game_over(board,player):
                                jumped_mod+=200
                            jumped_coord = [new_coord]
                        else:
                            break
                    else:
                        break
                # backward motion
                i = 1
                jumps = 0              
                jumped_mod = 0
                jumped_coord = []
                while i < N:
                    new_coord = (coord[0]-i*key[0],coord[1])
                    if new_coord[0]>-1 and new_coord[0]<N and board[coord_index(new_coord,N)] == '.':
                        all_moves.append([value+value_mod*(enemy_strength-1+jumped_mod),coord,new_coord,jumped_coord])
                        i+=1
                    elif new_coord[0]>0 and new_coord[0]<N-1 and board[coord_index(new_coord,N)] in key2:
                        next_coord = (new_coord[0]-key[0],new_coord[1])
                        if board[coord_index(next_coord,N)] == '.' and jumps == 0:
                            i+=1
                            jumps+=1
                            jumped_mod = key2.index(board[coord_index(new_coord,N)])*2+6
                            if game_over(board,player):
                                jumped_mod+=200
                            jumped_coord = [new_coord]
                        else:
                            break
                    else:
                        break
                # right motion
                i = 1
                jumps = 0              
                jumped_mod = 0              
                jumped_coord = []
                while i < N:
                    new_coord = (coord[0],coord[1]+i)
                    if new_coord[1]<N and board[coord_index(new_coord,N)] == '.':
                        all_moves.append([value+value_mod*(enemy_strength-1+jumped_mod),coord,new_coord,jumped_coord])
                        i+=1
                    elif new_coord[1]<N-1 and board[coord_index(new_coord,N)] in key2:
                        next_coord = (new_coord[0],new_coord[1]+1)
                        if board[coord_index(next_coord,N)] == '.' and jumps == 0:
                            i+=1
                            jumps+=1
                            jumped_mod = key2.index(board[coord_index(new_coord,N)])*2+6
                            if game_over(board,player):
                                jumped_mod+=200
                            jumped_coord = [new_coord]
                        else:
                            break
                    else:
                        break
                # left motion
                i = 1
                jumps = 0              
                jumped_mod = 0              
                jumped_coord = []
                while i < N:
                    new_coord = (coord[0],coord[1]-i)
                    if new_coord[1]>-1 and board[coord_index(new_coord,N)] == '.':
                        all_moves.append([value+value_mod*(enemy_strength-1+jumped_mod),coord,new_coord,jumped_coord])
                        i+=1
                    elif new_coord[1]>0 and board[coord_index(new_coord,N)] in key2:
                        next_coord = (new_coord[0],new_coord[1]-1)
                        if board[coord_index(next_coord,N)] == '.' and jumps == 0:
                            i+=1
                            jumps+=1
                            jumped_mod = key2.index(board[coord_index(new_coord,N)])*2+6
                            if game_over(board,player):
                                jumped_mod+=200
                            jumped_coord = [new_coord]
                        else:
                            break
                    else:
                        break         
                # forward/right diagonal motion
                i = 1
                jumps = 0               
                jumped_mod = 0               
                jumped_coord = []
                while i < N:
                    new_coord = (coord[0]+i*key[0],coord[1]+i)
                    if new_coord[0]>-1 and new_coord[0]<N and new_coord[1]<N and board[coord_index(new_coord,N)] == '.':
                        all_moves.append([value+value_mod*(enemy_strength-1+jumped_mod),coord,new_coord,jumped_coord])
                        i+=1
                    elif new_coord[0]>0 and new_coord[0]<N-1 and new_coord[1]<N-1 and board[coord_index(new_coord,N)] in key2:
                        next_coord = (new_coord[0]+key[0],new_coord[1]+1)
                        if board[coord_index(next_coord,N)] == '.' and jumps == 0:
                            i+=1
                            jumps+=1
                            jumped_mod = key2.index(board[coord_index(new_coord,N)])*2+6
                            if game_over(board,player):
                                jumped_mod+=200
                            jumped_coord = [new_coord]
                        else:
                            break
                    else:
                        break         
                # forward/left diagonal motion
                i = 1
                jumps = 0              
                jumped_mod = 0                
                jumped_coord = []
                while i < N:
                    new_coord = (coord[0]+i*key[0],coord[1]-i)
                    if new_coord[0]>-1 and new_coord[0]<N and new_coord[1]>-1 and board[coord_index(new_coord,N)] == '.':
                        all_moves.append([value+value_mod*(enemy_strength-1+jumped_mod),coord,new_coord,jumped_coord])
                        i+=1
                    elif new_coord[0]>0 and new_coord[0]<N-1 and new_coord[1]>0 and board[coord_index(new_coord,N)] in key2:
                        next_coord = (new_coord[0]+key[0],new_coord[1]-1)
                        if board[coord_index(next_coord,N)] == '.' and jumps == 0:
                            i+=1
                            jumps+=1
                            jumped_mod = key2.index(board[coord_index(new_coord,N)])*2+6
                            if game_over(board,player):
                                jumped_mod+=200
                            jumped_coord = [new_coord]
                        else:
                            break
                    else:
                        break         
                # backward/right diagonal motion
                i = 1
                jumps = 0              
                jumped_mod = 0                
                jumped_coord = []
                while i < N:
                    new_coord = (coord[0]-i*key[0],coord[1]+i)
                    if new_coord[0]>-1 and new_coord[0]<N and new_coord[1]<N and board[coord_index(new_coord,N)] == '.':
                        all_moves.append([value+value_mod*(enemy_strength-1+jumped_mod),coord,new_coord,jumped_coord])
                        i+=1
                    elif new_coord[0]>0 and new_coord[0]<N-1 and new_coord[1]<N-1 and board[coord_index(new_coord,N)] in key2:
                        next_coord = (new_coord[0]-key[0],new_coord[1]+1)
                        if board[coord_index(next_coord,N)] == '.' and jumps == 0:
                            i+=1
                            jumps+=1
                            jumped_mod = key2.index(board[coord_index(new_coord,N)])*2+6
                            if game_over(board,player):
                                jumped_mod+=200
                            jumped_coord = [new_coord]
                        else:
                            break
                    else:
                        break         
                # backward/left diagonal motion
                i = 1
                jumps = 0              
                jumped_mod = 0                
                jumped_coord = []
                while i < N:
                    new_coord = (coord[0]-i*key[0],coord[1]-i)
                    if new_coord[0]>-1 and new_coord[0]<N and new_coord[1]>-1 and board[coord_index(new_coord,N)] == '.':
                        all_moves.append([value+value_mod*(enemy_strength-1+jumped_mod),coord,new_coord,jumped_coord])
                        i+=1
                    elif new_coord[0]>0 and new_coord[0]<N-1 and new_coord[1]>0 and board[coord_index(new_coord,N)] in key2:
                        next_coord = (new_coord[0]-key[0],new_coord[1]-1)
                        if board[coord_index(next_coord,N)] == '.' and jumps == 0:
                            i+=1
                            jumps+=1
                            jumped_mod = key2.index(board[coord_index(new_coord,N)])*2+6
                            if game_over(board,player):
                                jumped_mod+=200
                            jumped_coord = [new_coord]
                        else:
                            break
                    else:
                        break
    for move in all_moves:
        if move[0]>=200:
            return [move]
    return all_moves

# Max Value function for alpha/beta pruning
# - Treats move and board as the state
# - Passes through depth, player, N, and limit for helper functions and 
#   to determine when at maximum depth
def max_value(move,board,alpha,beta,depth,player,N,limit):
    if depth >= limit:
        return move[0]
    next_moves = all_moves(depth,move[0],board,N,player)
    if next_moves == []:
        return move[0]
    player = player_swap(player)
    depth+=1
    for move in next_moves:
        alpha = max(alpha, min_value(move,move_to_board(move,board,N),alpha,beta,depth,player,N,limit))
        if alpha>=beta:
            return alpha
    return alpha

# Min Value function for alpha/beta pruning
# - Treats move and board as the state
# - Passes through depth, player, N, and limit for helper functions and 
#   to determine when at maximum depth
def min_value(move,board,alpha,beta,depth,player,N,limit):
    if depth >= limit:
        return move[0]
    next_moves = all_moves(depth,move[0],board,N,player)
    if next_moves == []:
        return move[0]
    player = player_swap(player)
    depth+=1
    for move in next_moves:
        beta = min(beta,max_value(move,move_to_board(move,board,N),alpha,beta,depth,player,N,limit))
        if alpha >= beta:
            return beta
    return beta

# Toggles between players
def player_swap(player):
    if player == 'w':
        next_player = 'b'
    else:
        next_player = 'w'
    return next_player

# Finds best move
def find_best_move(board, N, player, timelimit):
    turn_over = time.time()+timelimit
    # Accounts for the case where there are no pieces to move
    # - Yields unchanged initial board, since there are no legal moves
    if player == 'b':
        pieces = ['b','B','$']
    else:
        pieces = ['w','W','@']
    if pieces[0] not in board and pieces[1] not in board and pieces[2] not in board:
        yield board
        return
    # Set initial minimax depth limit to 2 and yield answer. Then repeat:
    # - increase limit by 2 and yield better answer (as long as time allows)
    limit = 2
    while time.time() < turn_over:
        depth = 0
        max_moves = all_moves(depth,0,board,N,player)
        next_player = player_swap(player)
        depth+=1
        for move in max_moves:
            move[0] = min_value(move, move_to_board(move,board,N),-1000,1000,depth,next_player,N,limit)
        yield move_to_board(max(max_moves), board, N)
        limit+=2

if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise Exception("Usage: Raichu.py N player board timelimit")
        
    (_, N, player, board, timelimit) = sys.argv
    N=int(N)
    timelimit=int(timelimit)
    if player not in "wb":
        raise Exception("Invalid player.")

    if len(board) != N*N or 0 in [c in "wb.WB@$" for c in board]:
        raise Exception("Bad board string.")

    print("Searching for best move for " + player + " from board state: \n" + board_to_string(board, N))
    print("Here's what I decided:")
    for new_board in find_best_move(board, N, player, timelimit):
        print(new_board)
