# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 23:47:53 2020

@author: DreadEve
"""

import torch
import pandas as pd
import random
import copy
from konnect import board

#Adapted from Chris's code, but switched to a simple 6 by 7 board
#Plays on a board class object from the konnect file
#the following function takes a current board, and evaluates the best move for the provided player
#It does this by playing out ppmc random games for each possible move
#Whichever move gave the most number of wins, is the move the function will make




def montecarlo(brd): 
    """Inputs and board class object and performs random moves following """
    ppmc = 20 #(Random) Paths Per Move Count
    wincounter = torch.zeros(7)
    for k in range(7):
        #First, check to see if the column is full
        if brd.current_board[0][k] !=0:
            wincounter[k]= -1 # so it never picks this option
        else:
            for paths in range(ppmc):
                #Begin by dropping piece in current column
                workboard = copy.deepcopy(brd)
                workboard.drop_piece(k)
                while workboard.check_winner() == False:
                    #Tries to drop a piece into one of the valid column actions
                    #(Should) only receive error if board is completely full (tie)
                    try:
                        workboard.drop_piece(random.choice(workboard.actions()))
                    except:
                        break
                #So, when the game ends, the last player to make a move will have won
                #Since the drop_piece functions changes the current player
                #Thus, when the game ends the active player is the loser (or tie)
                if workboard.player == 3 - brd.player and workboard.check_winner() == True:
                    wincounter[k] +=1
                else:
                    pass
    print(wincounter)
    #Outputs the given board with the move with the highest wins
    return brd.drop_piece(torch.argmax(wincounter))                     
                    
#We may need to vectorize brd.current board vs brd, so we allow it to do both
def vectorize(brd):
    """
    Takes a board or tensor and outputs it as a string
    """
    try:
        flat = torch.flatten(brd.current_board)
    except:
        flat = torch.flatten(brd)
        #the item() remove the tensor attribute, we convert to integer to remove float, then string
    return ''.join([str(int(x.item())) for x in flat])

#I don't even think this function is necessary.
def devectorize(state):
    """
    Takes a database string and converts it into a torch tensor
    """
    tense = torch.empty(42)
    for i in range(len(state)):
        tense[i] = float(state[0])
    #Reshape does exactly what it sounds like; takes the tensor and turns it into 6x7
    return tense.reshape([6,7])


    #Record player 1 states and player 2 states separately for simplicity
    #I guess filename isn't a necessary argument but whatever
    #database is ["States", "Visits", "Value]
def recordgsv(filename,brd, won):   #Record game state value
    """
    This function takes a board state (or vectorized state), converts it to a vector, and stores it in a csv file.
    It also stores and updates the value and total number of visits for that game state.
    won variable is -1, 0, 1 for loss, tie, and win respectively
    """
    #load the dataframe
    df = pd.read_csv(filename, dtype = {"State": str})
    try:
        thestate = vectorize(brd)
    except:
        thestate = brd
    #in checks against the index, values specifies to 
    if thestate in df["State"].values:
        #loc finds the appropriate entry
        df.loc[df["State"] == thestate, "Visits"] += 1
        #update average formula.
        #loc looks in a column for a specific value(s), then pulls the appropriate
        #value from the other column
        df.loc[df["State"] == thestate, "Value"] += \
            (won - df.loc[df["State"] == thestate, "Value"]) \
            /df.loc[df["State"] == thestate, "Visits"]
    else:
        df = df.append({"State": thestate, "Visits": 1, "Value": won}, ignore_index = True)
    #Overwrites the old database. index = false or it brings the index col into the csv
    df.to_csv(filename, mode = 'w', index = False)
        
    
    
#Load game state value
def loadgsv(brd):
    """
    Given a board state, look at the database and move towards the state with the 
    highest value. This is an epsilon greedy policy, and has a changeable parameter
    epsilon which determines exploration chance.
    """
    file = ""
    epsilon = random.random()
    #Exploration: check beginning otherwise don't bother with the rest of the code
    if epsilon <= 0.01:
        return brd.drop_piece(random.choice(brd.actions()))
    else:
        if brd.player == 1:
            file = "konnectp1.csv"
        elif brd.player == 2:
            file = "konnectp2.csv"
        else:
            print("Player value error")
        df = pd.read_csv(file, dtype = {"State": str})
        wincounter = torch.zeros(7)
        #Loop through different moves and pick the highest value state
        for col in brd.actions():
            workboard = copy.deepcopy(brd)
            workboard.drop_piece(col)
            if vectorize(workboard) in df["State"].values:
                wincounter[col] = df.loc[df["State"] == vectorize(workboard), "Value"]
            else:
                wincounter[col] = 0
        if sum(wincounter) <= 0:
            return montecarlo()
        else:
            print(wincounter + " Values")
            return brd.drop_piece(torch.argmax(wincounter))
            
    
                
            
        

                

