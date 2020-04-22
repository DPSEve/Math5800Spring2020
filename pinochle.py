# Two Handed Pinochle
# Only one app on the Play Store has Two Handed Pinochle. It only has one difficulty setting. No app has two handed Binokel!
# To-Do Later: Bezique, Chinese Bezique, Polish Bezique

import random as rnd
from colorama import Fore, Back, Style
import os

hrt = "♥" #259 through 262 using ALT+CODE on WIN10
spd = "♠"
clb = "♣"
dmn = "♦"

ranks = [0, 1, 2, 3, 4, 5]
ranknames = ["Nine", "Jack", "Queen", "King", "Ten", "Ace"]
rankshortnames = ["9", "J", "Q", "K", "T", "A"]
suits = [0, 1, 2, 3]
suitnames = ["Clubs", "Diamonds", "Hearts", "Spades"]
suitshortnames = [clb, dmn, hrt, spd]
values = [0, 2, 3, 4, 10, 11]

colors = True
german = False

if german == True: #For Binokel
    ranknames = ["Seven", "Under", "Over", "King", "Ten", "Deuce"]
    suitnames = ["Acorns", "Bells", "Hearts", "Leaves"]
    rankshortnames = ["7", "U", "O", "K", "X", "D"]
    suitshortnames[1] = "●" #Not sure the code, found online, Unicode 25C0, BLACK CIRCLE


def melds(trumps): #returns list of all melds in the form [ ..., [ [ list of cards in [rank, suit] form ] , point value, class, meld name] ,... ]
    #class is used to determine whether or not re-melding is allowed.
    nottrumps = [0, 1, 2, 3]
    nottrumps.remove(trumps) #list of non-trump suits

    #Recall that runs replace royal marriages. Not accounted for here.
    run = [ [[1, trumps], [2, trumps], [3, trumps], [4, trumps], [5, trumps]] , 150, 0, "Run in Trumps" ] # Run, 150 points
    royalmarriage = [ [[2, trumps], [3, trumps]], 40, 0, "Royal Marriage"] # Royal Marriage (King and Queen of trumps), 40 points

    commonmarriage1 = [ [[2, nottrumps[0]], [3, nottrumps[0]]], 20, 0, "Common Marriage in " + suitnames[nottrumps[0]]] # Common Marriage 1 (King and Queen of non-trump), 20 points
    commonmarriage2 = [ [[2, nottrumps[1]], [3, nottrumps[1]]], 20, 0, "Common Marriage in " + suitnames[nottrumps[1]]] # Common Marriage 2, 20 points
    commonmarriage3 = [ [[2, nottrumps[2]], [3, nottrumps[2]]], 20, 0, "Common Marriage in " + suitnames[nottrumps[2]]] # Common Marriage 3, 20 points
    dix = [ [[0, trumps]], 10, 0, "Dix, " + ranknames[0] + " of " + suitnames[trumps]] # Dix (Nine of Trumps), 10 points
    acesaround = [ [ [5, trumps], [5, nottrumps[0]], [5, nottrumps[1]], [5, nottrumps[2]] ], 100, 1, ranknames[5] + "s Around"] # Aces Around (one in each suit), 100 points
    kingsaround = [ [ [4, trumps], [4, nottrumps[0]], [4, nottrumps[1]], [4, nottrumps[2]] ], 80, 1, ranknames[3] + "s Around"] # Kings Around, 80 points
    queensaround = [ [ [3, trumps], [3, nottrumps[0]], [3, nottrumps[1]], [3, nottrumps[2]] ], 60, 1, ranknames[2] + "s Around"] # Queens Around, 60 points
    jacksaround = [ [ [2, trumps], [2, nottrumps[0]], [2, nottrumps[1]], [2, nottrumps[2]] ], 40, 1, ranknames[1] + "s Around"] # Jacks Around, 40 points

    #Recall that double Pinochle replaces Pinochle. Not accounted for here.
    pinochle = [ [[2, 3], [1, 1]], 40, 2, "Pinochle"] #Pinochle, Queen of Spades + Jack of Diamonds, 40 points
    doublepinochle = [ [[2, 3], [1, 1], [2, 3], [1, 1]], 300, 2, "DOUBLE PINOCHLE!"] #Double Pinochle. Two Pinochles. Make sure to check for this properly! 300 points
    meldlist = [run, royalmarriage, commonmarriage1, commonmarriage2, commonmarriage3, dix, acesaround, kingsaround, queensaround, jacksaround, pinochle, doublepinochle]
    return meldlist

class card: #card object class. suit and rank. can return short-strings and long-strings for itself. call [rank, suit] quickly via card.info. 
	def __init__(self, rank, suit):
		self.suit = suit
		self.suitname = suitnames[suit]
		self.rank = rank
		self.rankname = ranknames[rank]
		self.value = values[rank]
		self.info = [self.rank, self.suit]

	def cardname(self):
		return self.rankname + " of " + self.suitname
	def short(self):
		return showcard(self.rank, self.suit)
	def iscard(self, cardaslist): #cardaslist must be of the form [rank, suit]
                iscard = False
                if self.rank == cardaslist[0] and self.suit == cardaslist[1]:
                    iscard = True
                return iscard

def showcard(rank, suit): #Displays shorthand of card, colored if possible. e.g. "J♦" for Jack of Diamonds. 
	if colors == True:
		return "" + str(colormatch(suit)) + rankshortnames[rank] + suitshortnames[suit] + str(Style.RESET_ALL) + ""
	else: 
		return rankshortnames[rank] + suitshortnames[suit]
	
def colormatch(suit):
    if german == False:
        if suit == 0:
            return Fore.GREEN #Green Clubs (Clovers)
        if suit == 1:
            return Fore.YELLOW #Yellow Diamonds (Tiles), Blue is more common but looks bad in the terminal.
        if suit == 2:
            return Fore.RED #Red Hearts
        if suit == 3: 
            return "" #White (or black) Spades (Swords, Pikes - "Espada")
    if german == True:
        if suit == 0:
            return Fore.YELLOW #Yellow Acorns
        if suit == 3:
            return Fore.GREEN #Green Leaves
        if suit == 2:
            return Fore.RED #Red Hearts
        if suit == 1:
            return "" #White (or black) Bells
	    
class cardpile: #any collection of cards, including hands, decks, discard piles, trick piles, player meld areas... last item is top card, if order matters. 
	def __init__(self):
		self.pilelist = []

	def gendeck(self): #makes the whole deck
		for i in ranks:
			for j in suits:
				self.pilelist.append(card(i, j))
		self.shuffle()

	def shuffle(self):
		rnd.shuffle(self.pilelist)
		
	def count(self):
		return len(self.pilelist)

	def displaywhole(self): #returns whole pile as short-version strings inside | |'s. 
		if self.count() > 0:
			discardstring = ""
			for i in self.pilelist:
				discardstring += "|"+i.short()+"|"
			return discardstring
		else:
			return "Empty"
		    
	def topcard(self): #returns top card as card class type, or Empty string
		if len(self.pilelist) > 0:
			return self.pilelist[-1]
		else:
			return "Empty"

	def upcard(self): #returns bottom card as card class type, or Empty string
		if len(self.pilelist) > 0:
			return self.pilelist[0]
		else:
			return "Empty"

	def takecard(self, frompile, wherefrom = -1, whereto = -1): #takes card from frompile and places it in this pile. default is top to top. no error / length checking!
		self.pilelist.insert(whereto, frompile.pilelist.pop(wherefrom))

	def drawhand(self, deck, handsize=12): #draws handsize (12) from "deck", used for making hands
		for i in range(handsize):
			self.takecard(deck)
		self.sortsuits()
	
	def sortranks(self):
		issorted = False
		while issorted == False:
			didsomething = False
			for i in range(self.count() - 1):
				if self.pilelist[i].rank > self.pilelist[i+1].rank:
					self.pilelist[i], self.pilelist[i + 1] = self.pilelist[i + 1], self.pilelist[i]
					didsomething = True
				if self.pilelist[i].rank == self.pilelist[i+1].rank and self.pilelist[i].suit > self.pilelist[i+1].suit:
					self.pilelist[i], self.pilelist[i + 1] = self.pilelist[i + 1], self.pilelist[i]
					didsomething = True                                        
			if didsomething == False:
				issorted = True

	def sortsuits(self):
		issorted = False
		while issorted == False:
			didsomething = False
			for i in range(self.count() - 1):
				if self.pilelist[i].suit > self.pilelist[i+1].suit:
					self.pilelist[i], self.pilelist[i + 1] = self.pilelist[i + 1], self.pilelist[i]
					didsomething = True
				if self.pilelist[i].suit == self.pilelist[i+1].suit and self.pilelist[i].rank > self.pilelist[i+1].rank:
					self.pilelist[i], self.pilelist[i + 1] = self.pilelist[i + 1], self.pilelist[i]
					didsomething = True                                        
			if didsomething == False:
				issorted = True

def follower():
    return (leader + 1) % 2

def possiblemelds(player, trumps): #each card in meldarea list is of the form [card object, (melding) class]. Hand is a usual list of card objects. 
    hand = players[player][0]
    meldarea = players[player][1]
    allpossmelds = melds(trumps) #generates list of ALL possible melds for given trump
    playerpossmelds = []
    for i in range(3): #go through each class type
        availablecards = []
        for handcards in hand.pilelist:
            availablecards.append(handcards)
        for j in meldarea.pilelist:
            if j[1] != i: #melded card's class (j) does NOT match testing class (i) - available to use
                availablecards.append(j)
        for meldposs in allpossmelds:
            if meldposs[2] == i: #test meld's class matches current class we care about (i)
                isinhand = True #assume we have it, look for missing cards
                for neededcard in meldposs[0]:
                    haveit = False
                    for availcard in availablecards:
                        if availcard.iscard(neededcard):
                            haveit = True
                    if haveit == False:
                        isinhand = False
                if isinhand == True: #if pass test (have the meld), add meld to possibilities list.
                    playerpossmelds.append(meldposs)
    return playerpossmelds



    
# Procedure for a turn:
# 1.) Check for Dix-Swap.
# 2.) If NOT first turn and NOT play-off, ask Leader to choose from Meld-List, list of all their possible melds.
# 3.) Move meld cards to melding-area for player. Adjust score.
# 3.) Ask Lead to choose card to lead with from hand + melding-aira.
# 4.) Ask Follower to choose card to play. If in play-off, require following suit + victory if possible.
# 5.) Check who won trick. Move tricks to winner's trick-pile. Adjust score.
# 6.) If hand empty, end round. Start new round if needed. If draw-pile not empty, draw cards. If draw-pile becomes empty, trigger play-off. 

def turn():
    global deck, players, upcard
    leaderhand = players[leader][0]
    #1.) Dix-Swap
    for i in range(len(leaderhand)):
        if leaderhand[i].iscard([0, trumps]):
            if leaderhand[i].suit != upcard.suit or leaderhand[i].rank != upcard.rank:
                leaderhand.takecard(deck, 0)
                deck.takecard(leaderhand, i, 0)
                players[leader][3] += 10 #Add 10 points for Dix

    #2.) Choose From Meld-List

                
                
    


#Set-Up Here

deck = cardpile()
deck.gendeck()
deck.gendeck() #Need two decks for Pinochle!

players = [[], []] #Player format will be [hand, meldarea, trickswon, score] starting as [ empty cardpile, * , empty cardpile, 0 ]. *meldarea is list of elements of form [card object, melding class]
for i in players:
    for j in range(2):
        i.append(cardpile()) #Appends 3 piles - hand, meld area, and tricks won in that round (all empty for now)
    i.append(0) # Score is 0

players[0][0].drawhand(deck)
players[1][0].drawhand(deck)

print(deck.displaywhole())
print(players[0][0].displaywhole())
print(players[1][0].displaywhole())

leader = 1 #Player 0 is leading (younger hand), Player 1 is following (elder hand). 
upcard = deck.upcard()
trumps = upcard.suit + 0
# 1.)

for melds in possiblemelds(leader, trumps):
    print(melds[3])


# Standard AI Rules:
# Choose Highest Scoring Meld Whenever Possible
# If Hold 2 or More of "Around" Card, Hold.
# If Hold 1 of Pinochle, Hold.
# If Opponent Leads Ten and Have Ace, Always Play Ace, Unless Have 3/4 Aces Around and no spare.
# etc






