# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 23:47:53 2020

@author: DreadEve
"""

import numpy as np
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
    ppmc = 40 #(Random) Paths Per Move Count
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
                    

def vectorize(brd):
    """
    Takes a board and outputs it as a string
    """
    flat = torch.flatten(brd.current_board)
    vector = ""
    for i in range(len(flat)):
        #the item() remove the tensor attribute, we convert to integer to remove float, then string
        vector += str(int(flat[i].item()))
    return vector

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
    This function takes a board state, converts it to a vector, and stores it in a csv file.
    It also stores and updates the value and total number of visits for that game state.
    won variable is -1, 0, 1 for loss, tie, and win respectively
    """
    #load the dataframe
    df = pd.read_csv(filename)
    thestate = vectorize(brd)
    if thestate in df["State"]:
        #loc finds the appropriate entry
        df.loc[df["State"] == thestate, "Visits"] += 1
        #update average
        df.loc[df["State"] == thestate, "Value"] += \
            (won + df.loc[df["State"] == thestate, "Visits"]) \
            /df.loc[df["State"] == thestate, "Visits"]
    else:
        df = df.append({"State": thestate, "Visits": 1, "Value": won}, ignore_index = True)
    df.to_csv(filename, mode = 'w', index = False)
        
    
    
    
def retrievegsv(filename):
    """
    Opens up the database of state value pairs
    """


                

