# Connect Four for Spring 2020 Class with Jeremy Teitelbaum, Chris Hayes and Evelyn Nitch-Griffin
# M rows by N columns
# Each player can make one of N moves, or less if full. Places object in lowest free spot in column N.
# Win occurs if a move creates "four in a row" (can adjust to K in a row)

import numpy as np

def getparameters():
        #defaults
        cols = 7
        rows = 6
        connect = 4
        ppmc = 10
        try:
                testfile = open("parameters", "r")
        except FileNotFoundError:
                print("Creating empty parameter file.")
                testfile = open("parameters", "w")
        finally:
                testfile.close()
        parafile = open("parameters", "r")
        params = parafile.readlines()
        paramvector = [ ["columns", cols], ["rows", rows], ["inarow", connect], ["tries", ppmc]]
        for line in params:
                for J in paramvector:
                        if line.split("=")[0].strip().lower() == J[0]:
                                try:
                                        J[1] = int(line.split("=")[1].strip())
                                except TypeError:
                                        print("Formatting for " + J[0] + "in parameter file incorrect.")
        parafile.close()
        return cols, rows, connect, ppmc

def writeparameter():
        return 1

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
        global fullcolvec
        ppmc = 25 #(Random) Paths Per Move Count
        width = len(brd[0])
        wincounter = np.zeros([width])
        totalpaths = ppmc * width
        counter = 0
        for k in range(width):
                if fullcolvec[k] == False:
                        for paths in range(ppmc):
                                workboard = brd.copy()
                                workboard = placer(workboard, k, aip)
                                active = (aip % 2) + 1
                                while checkforwin(workboard) == 0:
                                        move = np.random.randint(width)
                                        if fullcolvec[move] == False:
                                                workboard = placer(workboard, np.random.randint(width), active)
                                                active = (active % 2) + 1
                                counter += 1
                                winner = checkforwin(workboard)
                                if winner == aip:
                                        wincounter[k] += 1
        print(str(wincounter) + " Player " + str(aip))
        return np.int(np.amin(np.where(wincounter == np.amax(wincounter))))


def recordgame(record, currentboard, winner = None):
        freezeboard = currentboard.copy()
        record.append(freezeboard)
        if winner == 1 or winner == 2:
                record.append(winner)
        return record

def invertgame(board): #converts game board to swap 1's and 2's
        global rows, cols
        shifter = np.ones((rows, cols))
        newboard = 3*shifter - board.copy()
        newnewboard = np.fmod(newboard, 3)
        return newnewboard

#Following two functions map board arrays to condensed strings (injectively) for reduced data storage.
    #Data dividers are & symbols.
    #Each column is recorded bottom-up. If it is a string of empty spots (zeros) we place one Z.
    #String goes: cols&rows&column1&column2& ... &column(cols)
    #Example for standard Connect 4: 7&6&Z&Z&121Z&22Z&121212&1Z&Z corresponds with:
    # 0 0 0 0 2 0 0 
    # 0 0 0 0 1 0 0 
    # 0 0 0 0 2 0 0 
    # 0 0 1 0 1 0 0
    # 0 0 2 2 2 0 0 
    # 0 0 1 2 1 1 0

    #Note that board state strings are not unique in the sense that swapping the 1's and 2's results in functionally the same state.
    #Will Store game state then &nextmoveK&..&..& where we give a number for the next move and whether it led to a W or a L, e.g. 4W.
    #Could just store win-loss vector for each possible move... i.e. &1W0L0&2W1L3&3W0L4&...
    #Could get rid of &'s by using Z's or length-vs-cols splitting!!
    
def convertstate(arrayboard):
    global cols, rows
    amp = "&"
    outstring = str(cols) + amp + str(rows) + amp
    for i in range(cols):
        for j in range(rows -1, -1, -1):
            if arrayboard[j][i] != 0:
                outstring += str(arrayboard[j][i])
            elif arrayboard[j][i] == 0:
                outstring += "Z&"
                break
            if j == 0 and i < cols - 1:
                outstring += "&"
    return outstring

def invertstate(stringboard):
    stringlist = stringboard.split("&")
    cols = int(stringlist[0])
    rows = int(stringlist[1])
    del stringlist[0]
    del stringlist[0]
    board = np.zeros((rows, cols), dtype=np.int8)
    for i in range(cols):
        nonzero = True
        for j in range(rows -1, -1, -1):
            toenter = list(stringlist[i])
            if nonzero == True:
                if toenter[rows - 1 - j] == "Z":
                    nonzero = False
            if nonzero == True:
                board[j][i] = int(toenter[rows - 1 - j])
            if nonzero == False:
                board[j][i] = 0
    return board




def getgamemode():
        print("Connect Four, Chris Hayes and Evelyn Nitch-Griffin")
        print("- - - - - - - - - - - - - - - - - - - - - - - - - ")
        print("1: Play against Computer")
        print("2: Watch Computer play itself (Pure Monte Carlo)")
        print("3: Two Players")
        print("Q: Quit")
        print("5: Watch Computer play itself (Machine Learning) (not done)")
        print("- - - - - - - - - - - - - - - - - - - - - - - - - ")
        validchoice = False
        while validchoice == False:
            validchoice = True
            choice = input("Make a choice:")
            if choice == "1":
                    return 1
            elif choice == "2":
                    return 2
            elif choice == "3":
                    return 3
            elif choice.lower() == "q" or choice.lower() == "quit":
                    return 4
            else:
                print("No valid option was entered. Try again!")
                validchoice = False

                
def aivsai():
    global cols, rows, connect, ppmc, board, gamerec, gameover, active
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
                    gamerec = recordgame(gamerec, board, whowon)
                    gameover = True
            else:
                    gamerec = recordgame(gamerec, board)
            
def playervsai():
    global cols, rows, connect, ppmc, board, gamerec, gameover, active
    print("Welcome to the game! Columns are identified from left to right as 1, 2, ..., " + str(cols))
    print("Enter the number corresponding to the column to make your move.")
    while gameover == False:
        print(board)
        move = input("Which column to play? ")
        if move.upper() == "QUIT":
                print("Game has been force-quit.")
                break
        board = placer(board, int(move)-1, active)
        whowon = checkforwin(board)
        if whowon != 0:
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
            
def playervsplayer():
    global cols, rows, connect, ppmc, board, gamerec, gameover, active
    while gameover == False:
        print(board)
        move = input("Which column to play in, Player " + str(active) + "?")
        if move.upper() == "QUIT":
                print("Game has been force-quit.")
                break
        board = placer(int(move)-1, active, board)
        active = (active % 2) + 1
        whowon = checkforwin(board)
        if whowon != 0:
                print(board)
                print("Player " + str(whowon) + " has  won!")
                break

def getmove(before, after): #gets column move between adjacent states. returns none if not adjacent.
    difference = after - before
#    print(difference)
    location = np.where(difference != 0)
#    print(location)
#    print(location[1])
    return int(location[1]), int(difference[location[0], location[1]])

def FGRconvert(gamerec): #converts to list, each item is a string like gamestate&&M1:4:W2 to mean player 1 made a move in column 4 and at the end player 2 won
        TD = ""
        for i in range(len(gamerec) - 3):
                TD += convertstate(gamerec[i])+"\n"
        splitTD = TD.split("\n")
        for i in range(len(splitTD) - 2):
                move, who = getmove(gamerec[i], gamerec[i+1])
                splitTD[i] += "&M" + str(who) + ":" + str(move) + ":W" + str(gamerec[-1])+ "\n"
        return splitTD


#database format is gamestate&&0

def addgamedata(gamedata, file): #uses format as in result of FGRconvert
        with open(file, "r") as db:
                data = db.readlines()
                
        for gamestate in gamedata:
                splitted = list(gamestate)
                winner = splitted[-1]
                nextmove = splitted[-4]
                nextmover = splitted[-6]
                length = len(gamestate)
                stateonly = gamestate.split("&&")[0]

                for line in data:
                        if line.split("&&")[0] == stateonly:
                                pass
                        pass
                

# Main Code Runs Here


gameover = False
active = 1
cols, rows, connect, ppmc = getparameters()
board = np.zeros((rows, cols), dtype=np.int8)
gamerec = []
fullcolvec = [False]*cols

choosemode = getgamemode()
if choosemode == 4: #4 is Quit
    print("Quit the program.")
if choosemode == 2: #AI vs AI
    aivsai()
if choosemode == 1:
    playervsai()
if choosemode == 3:
    playervsplayer()
gamedata = FGRconvert(gamerec)
addgamedata(gamedata, database)

    
"""
board[5][1] = 1
board[5][2] = 1
board[5][3] = 2
board[4][2] = 1
board[4][3] = 2
print(board)
conv = convertstate(board)
print(conv)
backboard = invertstate(conv)
print(backboard)
"""

"""
def addtodatabase(FGR): #FGR is Finished Game Record, a list of board game states and an integer indicator at the end of who won.
        gamelength = len(FGR) - 2 #last element is winner. 2nd to last element is copy of final game state. 
        winner = FGR[-1]
        if winner == 1: #convert to player 2 playing and winning only
                for gamestate in FGR[gamelength]:
                        gamestate = invertgame(gamestate)
        winner = 2
        #data is formatted as gamestate&wincount&totalgames
        database = open("database", "w+")
        statedata = database.readlines()
        towrite = []
        for gamestate in FGR[gamelength]:
                for line in statedata:
                        lineD = line.split("&")
                        if gamestate == np.asarray(lineD[0]):
                                lineD[2] += int(lineD[2])
                                if FGR[-1] == winner: #always 2
                                        lineD[1] += int(lineD[1])
                                else:
                                        pass
                                towrite.append(lineD[0] + "&" + str(lineD[1]) + "&" + str(lineD[2]))
                        else:
                                towrite.append(str(gamestate)+"&1&1")
        database.writelines(towrite)
        database.close()
"""
