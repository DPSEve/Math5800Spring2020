# Two Handed Pinochle / Binokel
# To-Do Later: Bezique, Chinese Bezique, Polish Bezique, Sechsundsechzig, Schnapsen
# All of these games are fundamentally the same, with the only major differences in deck size, hand size, point value, and when/what melding is allowed. 

import random as rnd
from colorama import Fore, Back, Style
import os

colors = True #uses colors in terminal. 
german = False #switches from standard French suits / ranks to German suits / ranks (see below), will need to swap Seven with Nine for Schnapsen/66 (much later)
winningscore = 1000
tieincrement = 250

hrt = "♥"  # 259 through 262 using ALT+CODE on WIN10
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

#pinochle melds placed here so I can reference them globally to make sure i don't have double pinochle (see possiblemelds function) 

pinochle = [[[2, 3], [1, 1]], 40, 2, "Pinochle"]  # Pinochle, Queen of Spades + Jack of Diamonds, 40 points
doublepinochle = [[[2, 3], [1, 1], [2, 3], [1, 1]], 300, 2, "Double Pinochle"]  # Double Pinochle. Two Pinochles. Make sure to check for this properly! 300 points

if german == True:  # For Binokel
    ranknames = ["Seven", "Under", "Over", "King", "Ten", "Deuce"]
    suitnames = ["Acorns", "Bells", "Hearts", "Leaves"]
    rankshortnames = ["7", "U", "O", "K", "X", "D"]
    suitshortnames[1] = "●"  # Not sure the code, found online, Unicode 25C0, BLACK CIRCLE


def melds(trumps):  # returns list of all melds in the form [ ..., [ [ list of cards in [rank, suit] form ] , point value, class, meld name string] ,... ]
    # class is used to determine whether or not re-melding is allowed.
    nottrumps = [0, 1, 2, 3]
    nottrumps.remove(trumps)  # list of non-trump suits

    # Recall that runs replace royal marriages. Not accounted for here.
    run = [[[1, trumps], [2, trumps], [3, trumps], [4, trumps], [5, trumps]], 150, 0, "Run in Trumps"]  # Run, 150 points
    royalmarriage = [[[2, trumps], [3, trumps]], 40, 0, "Royal Marriage in " + suitnames[trumps]]  # Royal Marriage (King and Queen of trumps), 40 points
    commonmarriage1 = [[[2, nottrumps[0]], [3, nottrumps[0]]], 20, 0, "Common Marriage in " + suitnames[nottrumps[0]]]  # Common Marriage 1 (King and Queen of non-trump), 20 points
    commonmarriage2 = [[[2, nottrumps[1]], [3, nottrumps[1]]], 20, 0, "Common Marriage in " + suitnames[nottrumps[1]]]  # Common Marriage 2, 20 points
    commonmarriage3 = [[[2, nottrumps[2]], [3, nottrumps[2]]], 20, 0, "Common Marriage in " + suitnames[nottrumps[2]]]  # Common Marriage 3, 20 points
    dix = [[[0, trumps]], 10, 0, "Dix, " + ranknames[0] + " of " + suitnames[trumps]]  # Dix (Nine of Trumps), 10 points
    acesaround = [[[5, trumps], [5, nottrumps[0]], [5, nottrumps[1]], [5, nottrumps[2]]], 100, 1, ranknames[5] + "s Around"]  # Aces Around (one in each suit), 100 points
    kingsaround = [[[3, trumps], [3, nottrumps[0]], [3, nottrumps[1]], [3, nottrumps[2]]], 80, 1, ranknames[3] + "s Around"]  # Kings Around, 80 points
    queensaround = [[[2, trumps], [2, nottrumps[0]], [2, nottrumps[1]], [2, nottrumps[2]]], 60, 1, ranknames[2] + "s Around"]  # Queens Around, 60 points
    jacksaround = [[[1, trumps], [1, nottrumps[0]], [1, nottrumps[1]], [1, nottrumps[2]]], 40, 1, ranknames[1] + "s Around"]  # Jacks Around, 40 points

    # Recall that double Pinochle replaces Pinochle. Not accounted for here.
#    pinochle = [[[2, 3], [1, 1]], 40, 2, "Pinochle"]  # Pinochle, Queen of Spades + Jack of Diamonds, 40 points
#    doublepinochle = [[[2, 3], [1, 1], [2, 3], [1, 1]], 300, 2, "Double Pinochle"]  # Double Pinochle. Two Pinochles. Make sure to check for this properly! 300 points
    meldlist = [run, royalmarriage, commonmarriage1, commonmarriage2, commonmarriage3, dix, acesaround, kingsaround, queensaround, jacksaround, pinochle, doublepinochle]
    return meldlist


class card:  # card object class. suit and rank. can return short-strings and long-strings for itself. call [rank, suit] quickly via card.info.
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

    def iscard(self, cardaslist):  # cardaslist must be of the form [rank, suit]
        iscard = False
        if self.rank == cardaslist[0] and self.suit == cardaslist[1]:
            iscard = True
        return iscard


def showcard(rank, suit):  # Displays shorthand of card, colored if possible. e.g. "J♦" for Jack of Diamonds.
    if colors == True:
        return "" + str(colormatch(suit)) + rankshortnames[rank] + suitshortnames[suit] + str(Style.RESET_ALL) + ""
    else:
        return rankshortnames[rank] + suitshortnames[suit]


def colormatch(suit):
    if german == False:
        if suit == 0:
            return Fore.GREEN  # Green Clubs (Clovers)
        if suit == 1:
            return Fore.YELLOW  # Yellow Diamonds (Tiles), Blue is more common but looks bad in the terminal.
        if suit == 2:
            return Fore.RED  # Red Hearts
        if suit == 3:
            return ""  # White (or black) Spades (Swords, Pikes - "Espada")
    if german == True:
        if suit == 0:
            return Fore.YELLOW  # Yellow Acorns
        if suit == 3:
            return Fore.GREEN  # Green Leaves
        if suit == 2:
            return Fore.RED  # Red Hearts
        if suit == 1:
            return ""  # White (or black) Bells


class cardpile:  # any collection of cards, including hands, decks, discard piles, trick piles, player meld areas... last item is top card, if order matters.
    def __init__(self):
        self.pilelist = []

    def gendeck(self):  # makes the whole deck
        for i in ranks:
            for j in suits:
                self.pilelist.append(card(i, j))
        self.shuffle()

    def shuffle(self):
        rnd.shuffle(self.pilelist)

    def count(self):
        return len(self.pilelist)

    def displaywhole(self):  # returns whole pile as short-version strings inside | |'s.
        if self.count() > 0:
            discardstring = ""
            for i in self.pilelist:
                discardstring += "|" + i.short() + "|"
            return discardstring
        else:
            return "Empty"

    def topcard(self):  # returns top card as card class type, or Empty string
        if len(self.pilelist) > 0:
            return self.pilelist[-1]
        else:
            return "Empty"

    def upcard(self):  # returns bottom card as card class type, or Empty string
        if len(self.pilelist) > 0:
            return self.pilelist[0]
        else:
            return "Empty"

    def takecard(self, frompile, wherefrom=-1,
                 whereto=-1):  # takes card from frompile and places it in this pile. default is top to top. no error / length checking!
        self.pilelist.insert(whereto, frompile.pilelist.pop(wherefrom))

    def drawhand(self, deck, handsize=12):  # draws handsize (12) from "deck", used for making hands
        for i in range(handsize):
            self.takecard(deck)
        self.sortsuits()

    def sortranks(self):
        issorted = False
        while issorted == False:
            didsomething = False
            for i in range(self.count() - 1):
                if self.pilelist[i].rank > self.pilelist[i + 1].rank:
                    self.pilelist[i], self.pilelist[i + 1] = self.pilelist[i + 1], self.pilelist[i]
                    didsomething = True
                if self.pilelist[i].rank == self.pilelist[i + 1].rank and self.pilelist[i].suit > self.pilelist[
                    i + 1].suit:
                    self.pilelist[i], self.pilelist[i + 1] = self.pilelist[i + 1], self.pilelist[i]
                    didsomething = True
            if didsomething == False:
                issorted = True

    def sortsuits(self):
        issorted = False
        while issorted == False:
            didsomething = False
            for i in range(self.count() - 1):
                if self.pilelist[i].suit > self.pilelist[i + 1].suit:
                    self.pilelist[i], self.pilelist[i + 1] = self.pilelist[i + 1], self.pilelist[i]
                    didsomething = True
                if self.pilelist[i].suit == self.pilelist[i + 1].suit and self.pilelist[i].rank > self.pilelist[
                    i + 1].rank:
                    self.pilelist[i], self.pilelist[i + 1] = self.pilelist[i + 1], self.pilelist[i]
                    didsomething = True
            if didsomething == False:
                issorted = True


def follower():
    return (leader + 1) % 2


def possiblemelds(player,
                  trmp):  # each card in meldarea list is of the form [card object, (melding) class]. Hand is a usual list of card objects.
    hand = players[player][0]
    meldarea = players[player][1]
    allpossmelds = melds(trmp)  # generates list of ALL possible melds for given trump
    playerpossmelds = []
    for i in range(3):  # go through each class type
        availablecards = []
        for handcards in hand.pilelist:
            availablecards.append(handcards)
        for j in meldarea.pilelist:
            if j[1] != i:  # melded card's class (j) does NOT match testing class (i) - available to use
                availablecards.append(j)
        for meldposs in allpossmelds:
            if meldposs[2] == i:  # test meld's class matches current class we care about (i)
                isinhand = True  # assume we have it, look for missing cards
                for neededcard in meldposs[0]:
                    haveit = False
                    for availcard in availablecards:
                        if availcard.iscard(neededcard):
                            haveit = True
                    if haveit == False:
                        isinhand = False
                if isinhand == True:  # if pass test (have the meld), add meld to possibilities list.
                    playerpossmelds.append(meldposs)

    #exception for double pinochle - make sure we actually have two copies. usual testing method only asks if a card is in the hand so this is necessary. 
    if doublepinochle in playerpossmelds:
        QScount = 0
        JDcount = 0
        for handcards in hand.pilelist:
            if handcards.iscard([2, 3]):
                QScount += 1
            if handcards.iscard([1, 1]):
                JDcount += 1
        if QScount < 2 or JDcount < 2:
            playerpossmelds.remove(doublepinochle)
    
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
    global deck, players, upcard, isfirstturn, isplayoff
    leaderhand = players[leader][0].pilelist

    # 1.) Dix-Swap
    for i in range(len(leaderhand)):
        if leaderhand[i].iscard([0, trump]):
            if upcard.rank != 0:
                if leaderhand[i].suit != upcard.suit or leaderhand[i].rank != upcard.rank:
                    print("Exchanged the " + ranknames[0] + " of " + suitnames[trump] + " in your hand for the upcard, the " + upcard.cardname() + ". +10 points.")
                    players[leader][0].takecard(deck, 0)
                    deck.takecard(players[leader][0], i, 0)
                    print("Upcard:" + deck.upcard().short())
                    print("New Hand:" + players[leader][0].displaywhole())
                    players[leader][3] += 10  # Add 10 points for Dix
                    break

    # 2.) Choose From Meld-List
    choicenum = -1  # default is no melding
    if isfirstturn == True:  # Skip this step if it's the first turn.
        isfirsturn = False
    elif isplayoff == False:  # Normal procedure before playoff
        currentmeldlist = possiblemelds(leader, trump)
        if len(currentmeldlist) > 0:  # Check if there is a meld at all before presenting options
            for i in range(len(currentmeldlist)):
                print("Option " + str(i+1) + ": " + currentmeldlist[i][3] + ", " + str(currentmeldlist[i][1]) + " points.")
            print("Or, enter 0 to not meld at all.")
            validchoice = False
            while validchoice == False:
                choice = input(
                    "Choose an option:")  # Later will allow input of names as well as numbers, e.g. 'marriage' if there's only one marriage or 'trump marriage' or 'aces around' et cetera.
                try:
                    choicenum = int(choice) - 1
                    if choicenum >= -1 and choicenum < len(currentmeldlist):
                        validchoice = True
                    else:
                        print("Not a valid option!")
                except:
                    print("Not a valid option (or even an integer)!")

    # 3.) Move Melds to Melding-Area

    if choicenum != -1:  # Makes sure a meld was requested
        pass


# Set-Up Here

isplayoff = False
isfirstturn = True

deck = cardpile()
deck.gendeck()
deck.gendeck()  # Need two decks for Pinochle!

players = [[],
           []]  # Player format will be [hand, meldarea, trickswon, score] starting as [ empty cardpile, * , empty cardpile, 0 ]. *meldarea is list of elements of form [card object, melding class]
for i in players:
    for j in range(3):
        i.append(cardpile())  # Appends 3 piles - hand, meld area, and tricks won in that round (all empty for now)
    i.append(0)  # Score is 0

players[0][0].drawhand(deck)
players[1][0].drawhand(deck)

print("Deck:" + deck.displaywhole())
print("Upcard:" + deck.upcard().short())
print("----------------")
leader = 0  # Player 0 is leading (younger hand), Player 1 is following (elder hand).
upcard = deck.upcard()
trump = upcard.suit + 0
# 1.)
print(leader)
print(players[0][0].displaywhole())
for meld in possiblemelds(leader, trump):
    print(meld[3])
print("----------------")
print(follower())
print(players[1][0].displaywhole())
for meld in possiblemelds(follower(), trump):
    print(meld[3])

turn()
turn()
turn()
# Standard AI Rules:
# Choose Highest Scoring Meld Whenever Possible
# If Hold 2 or More of "Around" Card, Hold.
# If Hold 1 of Pinochle, Hold.
# If Opponent Leads Ten and Have Ace, Always Play Ace, Unless Have 3/4 Aces Around and no spare.
# etc






