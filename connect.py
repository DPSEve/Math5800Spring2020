# Connect Four
# M rows by N columns
# Each player can make one of N moves, or less if full.
# Win occurs if a move create "four in a row" (can adjust to K in a row)
# For now, put interface and game in some file. But make sure to use separate functions.

#Game
#step 1: make M x N grid (list in list or numpy ternary array: empty, player 1 piece, player 2 piece)
#step 2: get a move choice, check if legal first
#step 3: place move. check if a win occurs. go back to 2.

#Input: straightforward. display game. ask for a column.

#AI:
#Way 1: Look for all K-1 paths by opponent. Block. Otherwise choose to extend a longest path if it won't give a K-1. Otherwise random.
#Way 2: Consider all up-to-N possible moves. Generate random games to completion for each move. Choose move that gave most wins.
#Way 3: Get large data set of games. Use M*N independent variable linear regression on state space (no need to know move order) to choose move?
#More 3: Doesn't make sense? Find "close" games in data set. Find best move among those. Do that move?

#Could regress: (close state spaces, next move(s): win value). Choose move based on value of "next moves" column; highest value is chosen 

#Could use (all state spaces: win value) somehow? then place current state and look at ball. but finding elements in that ball might be... difficult? Point is to use regression after the fact. 

import numpy as np

cols =  7 #columns = number of move choices upper bound
rows = 6 #rows are rows
connect = 4 #number in a row to connect

board = np.zeros((rows, cols), dtype=np.int8)

def placer(movechoice, player): #Drops player value into movechoice columns
	global board
	for i in range(rows):
		if board[rows - i - 1][movechoice] == 0:
			board[rows - i - 1][movechoice] = player
			break

def checkforwin(): #Assumes only one win state can exist. More efficient to check neighbors of immediate moves.
	won = False
	winner = 0
	#Check Verticals
	for i in range(rows - connect+1):
		for j in range(cols):
			plyval = board[i][j]
			if plyval != 0:
				count = 0
				for k in range(connect):
					if board[i+k][j] == plyval:
						count += 1
					if count == connect:
						won = True
						winner = plyval
						return winner
        #Check Horizontals
	for i in range(rows):
		for j in range(cols - connect +1):
			plyval = board[i][j]
			if plyval != 0:
				count = 0
				for k in range(connect):
					if board[i][j+k] == plyval:
						count+=1
					if count == connect:
						won = True
						winner = plyval
						return winner
	#Check Diagonals \

	for i in range(rows - connect):
		for j in range(cols - connect):
			plyval = board[i][j]
			if plyval != 0:
				count = 0
				for k in range(connect):
					if board[i+k][j+k] == plyval:
						count +=1
					if count == connect:
						won = True
						winner = plyval
						return winner

	#Check Diagonals /

	for i in range(rows -1, connect-1, -1):
		for j in range(cols-1, connect-1, -1):
			plyval = board[i][j]
			if plyval !=0:
				count = 0
				for k in range(connect):
					if board[i - k][j-k] == plyval:
						count += 1
					if count == connect:
						won = True
						winner = plyval
						return winner
	# No winner found, return 0
	return winner

testboard = """
placer(1, 2)
placer(2, 2)
placer(3, 2)
placer(1, 2)
placer(2, 2)
placer(1, 2)
placer(1, 1)
placer(2, 1)
placer(3, 1)
placer(4, 1)
"""

#print(board)

gameover = False
active = 1

while gameover == False:
	print(board)
	move = input("Which column to play in, Player " + str(active) + "?")
	if move == "QUIT":
		print("Game has been force-quit.")
		break
	placer(int(move)-1, active)
	active = (active % 2) + 1
	whowon = checkforwin()
	if whowon != 0:
		print("Player " + str(whowon) + " has  won!")
		break

#whowon  = checkforwin()

#if whowon != 0:
#	print("Player " + str(whowon) + " won.")
#else:
#	print("No one has won.")

