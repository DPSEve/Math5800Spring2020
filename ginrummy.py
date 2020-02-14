#Gin Rummy Game
#Unfinished, currently no AI or Machine Learning implementation. 

import random as rnd

hrt = "♥" #259 through 262 using ALT+CODE on WIN10
spd = "♠"
clb = "♣"
dmn = "♦"

ranks = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
ranknames = ["Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King"]
rankshortnames = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]
suits = [0, 1, 2, 3]
suitnames = ["Clubs", "Diamonds", "Hearts", "Spades"]
suitshortnames = [clb, dmn, hrt, spd]
values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

def showcard(rank, suit):
	return rankshortnames[rank] + suitshortnames[suit]

class card:
	def __init__(self, rank, suit):
		self.suit = suit
		self.suitname = suitnames[suit]
		self.rank = rank
		self.rankname = ranknames[rank]
		self.value = values[rank]

	def cardname(self):
		return self.rankname + " of " + self.suitname
	def info(self):
		return [self.rank, self.suit]
	def short(self):
		return showcard(self.rank, self.suit)

class deck:
	def __init__(self):
		self.decklist = []
		for i in ranks:
			for j in suits:
				self.decklist.append(card(i, j))
		self.shuffle()

	def shuffle(self):
		decklist = rnd.shuffle(self.decklist)
	def count(self):
		return len(decklist)


class discardpile:
	def __init__(self):
		self.decklist = []

	def displaywhole(self):
		if len(self.decklist) > 0:
			discardstring = ""
			for i in self.decklist:
				discardstring += "|"+i.short()+"|"
			return discardstring
		else:
			return "Empty"
	def topcard(self):
		return self.decklist[-1]

	def startcard(self, pile):
		self.decklist.append(pile.decklist.pop())

class hand:
	def __init__(self, player):
		self.player = player
		self.contents = []

	def draw(self, pile):
		self.contents.append(pile.decklist.pop()) #Takes last-index (top) card of pile.

	def discard(self, yeet, pile):
		pile.append(yeet)
		self.contents.remove(yeet)

	def drawten(self, pile):
		for i in range(10):
			self.draw(pile)

	def showhand(self):
		handstring = ""
		for i in self.contents:
			handstring += "|"+i.short()+"|"
		return handstring

	#def ascendingsort(self):
	#	self.contents = sorted(self.contents

	#def matchingsort(self):

def sortrank(hand):
	return hand.contents

def divider():
	print("-----------------------------------")

def getmove():
	validmove = False
	while validmove == False:
		print("What would you like to do?")
		print("1: Take from Discard Pile")
		print("2: Take from Deck")
		move = input("Choice:")
		if move == "1" or move == "2":
			validmove = True
			return int(move)
		elif move == "Q" or move == "q" or move == "quit" or move == "QUIT":
			break
		else:
			print("Not a valid option.")
			divider()


maindeck = deck()
maindeck.shuffle()
listocards = ""
for i in maindeck.decklist:
	listocards = listocards + ("|" + showcard(i.rank, i.suit)+"|")
print(listocards)

player1 = hand(1)
player2 = hand(2)
player1.drawten(maindeck)
player2.drawten(maindeck)
print("Player 1's Hand: " + player1.showhand())
print("Player 2's Hand: " + player2.showhand())

dispile = discardpile()
dispile.startcard(maindeck)
divider()
print("Upcard is " + dispile.topcard().short())
print("What would you like to do?")
choice = getmove()
if choice == 1:
	player1.draw(dispile)
elif choice == 2:
	player1.draw(maindeck)
print(player1.showhand())


