# -*- coding: utf-8 -*-
"""
This file will run the main program, which will simulate some Connect 4 games using 
Monte Carlo Tree search and the Game State Value machine learning framework.
Additionally, it will use a Neural Network method as well.
@author: DreadEve
"""
import torch
import pandas as pd
import random
import copy
from konnect import board
from Monte import *


def mode():
    print("Connect Four with Chris Hayes and Evelyn Nitch-Griffin \n \
          - - - - - - - - - - - - - - - - \n\
          1. Monte vs Monte \n\
          2. Play Monte vs Monte but then record it \n\
          3. Machine Learning vs Monte \n\
          4. Machine Learning vs Machine Learning \n\
          Q. Quit! \n\
          - - - - - - - - - - - - - - - -")
    return input("Make a choice ")

def MvM():
    """
    Monte Carlo vs Monte Carlo
    """
    game = board()
    while game.check_winner() == False and len(game.actions()) !=0:
        montecarlo(game)
    print(game.current_board)
    
def MvMrecord():
    """
    Runs a game of Monte vs Monte, but records each move. At the end of the game,
    loop through the recorded states and update their state value pairs in the
    database.
    """
    game = board()
    #store board states in this double list of lists
    #player 1 states followed by player 2 states
    states = [[],[]]
    #Empty actions means a tie game
    while game.check_winner() == False and len(game.actions())!=0:
        montecarlo(game)
        '''Add the state you just moved into to the appropriate list
        again, game.player is the current move, so you add to the other players db
        only need to record states you move into to assess their value'''
        states[2-game.player].append(vectorize(game.current_board))
    print(game.current_board)
    #Tie game check
    if game.check_winner() == False and len(game.actions())!=0:
        winner = 1.5 # for my lame winner conversion below
    else:
        winner = 3 - game.player
    #Win = 1, Loss = -1, Tie = 0 
    for rec in states[0]:
        recordgsv("konnectp1.csv", rec, -2*winner + 3)
    for rec in states[1]:
        recordgsv("konnectp2.csv", rec, 2*winner - 3)
        
def LvM():
    """
    ML vs Monte Carlo
    """
    game = board()
    while game.check_winner() == False and len(game.actions()) !=0:
        if game.player == 1:
            loadgsv(game)
        else:
            montecarlo(game)
    print(game.current_board)
    
def LvL():
    """
    ML vs ML
    """
    game = board()
    while game.check_winner() == False and len(game.actions()) !=0:
        loadgsv(game)
    print(game.current_board)


#Here we shall begin the main code
choice = mode()

if choice == '1':
    MvM()
elif choice == '2':
    try:
        runs = int(input("How many games should it record?"))
        if runs > 5000 or runs < 0:
            print("That's a bit much")
        else:
            for i in range(runs):
                MvMrecord()
    except:
        print("Invalid choice")
elif choice == '3':
    LvM()
elif choice == '4':
    LvL()
elif choice == "Q":
    print("See ya")
else:
    print("Invalid Choice")




