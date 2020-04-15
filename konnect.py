# -*- coding: utf-8 -*-
"""
Connect four Code and Neural Network for Math5800 Spring 2020

This code contoins the board class and functions defined for it.

@author: Chris and Eve
"""
import numpy as np
import torch
import csv
import random


#Begin by defining a board class to act upon
#Contains initial start, state for current player (1 or 2), and current board status
class board:
    def __init__(self):
        self.init_board = torch.zeros(6,7) #initialize the boar as a torch tensor of zeros
        self.player = 1
        self.current_board = self.init_board
        
    #Drops the current player (player) "piece" into the the top column
    #Take note that python starts counting at 0, so the 6 by 7 tensor
    #Also note drop_piece changes the active player 
    def drop_piece(self, col):
        if self.current_board[0,col] != 0: #checks if top entry is 0
            return "Invalid Move"
        else: 
            #search from bottom of row (row 5) up for a 0 and turn it to player value
            for row in range(6):
                if self.current_board[5-row,col] == 0:
                    self.current_board[5-row,col] = self.player
                    break
            self.player = 3 - self.player #change current player
            
    #Returns all valid actions
    def actions(self):
        acts = []
        for col in range(7):
            if self.current_board[0,col] == 0:
                acts.append(col)
        return acts
    
    
    # Checks to see if somebody has won
    # Code should be able to tell based on who made the last move to see who won
    def check_winner(self):
        won = False
        #Check Verticals
        for row in range(3): #only need to check from top 3 rows
                for col in range(7):
                    plyval = self.current_board[row][col]
                    if self.current_board[row+1][col] == plyval and \
                        self.current_board[row+2][col]== plyval and \
                        self.current_board[row+3][col]== plyval and \
                            plyval != 0:
                            won = True
                    else:
                        pass
        #Check Horizontals
        for col in range(4): #only need to check from first 4 columns
                for row in range(6):
                    plyval = self.current_board[row][col]
                    if self.current_board[row][col+1] == plyval and \
                        self.current_board[row][col+2]== plyval and \
                        self.current_board[row][col+3]== plyval and \
                            plyval != 0:
                            won = True
                    else:
                        pass
        #Check Diagonals \
            #Sweep from left to right starting with top row, then going down
        for col in range(4): #only need to check from first 4 columns
                for row in range(3):
                    plyval = self.current_board[row][col]
                    if self.current_board[row+1][col+1] == plyval and \
                        self.current_board[row+2][col+2]== plyval and \
                        self.current_board[row+3][col+3]== plyval and \
                            plyval != 0:
                            won = True
                    else:
                        pass

        #Check Diagonals /
        #Sweep from right to left,starting at last column
        for col in range(4): #only need to check from first 4 columns
                for row in range(3):
                    plyval = self.current_board[row][6-col]
                    if self.current_board[row+1][5-col] == plyval and \
                        self.current_board[row+2][4-col]== plyval and \
                        self.current_board[row+3][3-col]== plyval and \
                            plyval != 0:
                            won = True
                    else:
                        pass
        return won
            
    #This function takes the current board and converts it into a vector
    #May be unecessary as pytorch allows tensor operations
    #Turns into a row vector, of each matrix row
    def vector(self):
        vec = torch.empty(42)
        count = 0
        for row in range(6):
            for col in range(7):
                vec[count] = self.current_board[row,col]
                count +=1
        return vec
                
            
