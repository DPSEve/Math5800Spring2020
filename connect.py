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

def placer(brd, movechoice, player): #Drops player value into movechoice row.
	for i in range(rows):
		if brd[rows - i - 1][movechoice] == 0:
			brd[rows - i - 1][movechoice] = player
			return brd
	return brd #Returns board with no changes if no possible move.

def checkforwin(brd): #Assumes only one win state can exist. More efficient to check neighbors of immediate moves.
	won = False
	winner = 0
	#Check Verticals
	for i in range(rows - connect+1):
		for j in range(cols):
			plyval = brd[i][j]
			if plyval != 0:
				count = 0
				for k in range(connect):
					if brd[i+k][j] == plyval:
						count += 1
					if count == connect:
						won = True
						winner = plyval
						return winner
        #Check Horizontals
	for i in range(rows):
		for j in range(cols - connect +1):
			plyval = brd[i][j]
			if plyval != 0:
				count = 0
				for k in range(connect):
					if brd[i][j+k] == plyval:
						count+=1
					if count == connect:
						won = True
						winner = plyval
						return winner
	#Check Diagonals \

	for i in range(rows - connect+1):
		for j in range(cols - connect+1):
			plyval = brd[i][j]
			if plyval != 0:
				count = 0
				for k in range(connect):
					if brd[i+k][j+k] == plyval:
						count +=1
					if count == connect:
						won = True
						winner = plyval
						return winner

	#Check Diagonals /

	for i in range(rows -1, connect-1, -1):
		for j in range(cols-1, connect-1, -1):
			plyval = brd[i][j]
			if plyval !=0:
				count = 0
				for k in range(connect):
					if brd[i - k][j-k] == plyval:
						count += 1
					if count == connect:
						won = True
						winner = plyval
						return winner

	if min(brd[0]) > 0:
		return -1 #Board filled, tie. 

	# No winner found, return 0
	return winner


def montecarlo(aip, brd): #Monte Carlo approach. aip is AI Player (a number, e.g. 1 or 2)
	ppmc = 10 #(Random) Paths Per Move Count
	width = len(brd[0])
#	print(str(width) + " WIDTH")
	wincounter = np.zeros([width])
	totalpaths = ppmc * width
	counter = 0
    #Begin by checking possible wins in the first column
	for k in range(width):
        #For each path per move, examine ppcm random games
		for paths in range(ppmc): 
            #Copy the board to experiment on
			workboard = brd.copy()
            #Break if already at a tie
			if checkforwin(workboard) == -1:
				break
			placer(workboard, k, aip)
			active = (aip % 2) + 1
		#	print(workboard)
            # Play random moves until you hit a winstate ppcm times
			while checkforwin(workboard) == 0:
				workboard = placer(workboard, np.random.randint(width), active)
#				print(workboard)
				active = (active % 2) + 1
			counter += 1
			#print( str( (counter/totalpaths) * 100 ) + " " + str(counter) + " " + str(totalpaths))
			#print(wincounter)
            #Count each game you win from that state, and tally them up
			winner = checkforwin(workboard)
			if winner == aip:
				wincounter[k] += 1
	print(str(wincounter) + " Player " + str(aip))
    #Make the move that generated the most winstates.
	return np.int(np.amin(np.where(wincounter == np.amax(wincounter))))



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


#AI VS AI CODE

while gameover == False:
	aimove = montecarlo(active, board)
	placer(board, aimove, active)
	active = (active % 2) + 1
	whowon = checkforwin(board)
	if whowon != 0:
		print(board)
		if whowon == 1:
			print("First AI Won")
		elif whowon == 2:
			print("Second AI Won")
		else:
			print("TIE")
		gameover = True

#ONE PLAYER VS AI CODE
"""
while gameover == False:
	print(board)
	move = input("Which column to play? ")
	if move == "QUIT":
		print("Game has been force-quit.")
		break
	board = placer(board, int(move)-1, active)
	whowon = checkforwin(board)
	if whowon !=0:
		print(board)
		print("You won!")
		break
	aimove = montecarlo(2, board)
	placer(board, aimove, 2)
	print("The AI played in column " + str(aimove+1) + ".")
	whowon = checkforwin(board)
	if whowon != 0:
		print(board)
		print("The computer won! :(")
		break

"""

#TWO PLAYER GAME CODE

"""
while gameover == False:
	print(board)
	move = input("Which column to play in, Player " + str(active) + "?")
	if move == "QUIT":
		print("Game has been force-quit.")
		break
	board = placer(int(move)-1, active, board)
	active = (active % 2) + 1
	whowon = checkforwin(board)
	if whowon != 0:
		print(board)
		print("Player " + str(whowon) + " has  won!")
		break
"""
#whowon  = checkforwin()

#if whowon != 0:
#	print("Player " + str(whowon) + " won.")
#else:
#	print("No one has won.")

