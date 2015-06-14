#from player import Player
from random import randint
from Card import *

#draw superclass
class Draw(object):
	def __init__(self, player):
		self.player = player
		
	def calculate_total(self):
		total = 0
		for card in self.player.cards:
			if card.number == 10 or card.number == "jack" or card.number == "queen" or card.number == "king":
				total += 0
			elif card.number == "ace":
				total += 1
			else:
				total += card.number
		return total % 10
	
	def draw(self):
		pass

#draw subclass: randomly picks wether or not to draw using python randint method
class RandomDraw(Draw):
	def draw(self):
		option = randint(0,1)
		if option == 1:
			#draw
			#print "draw"
			self.player.ask_limit += 1
			return True
		else:
			#dont add a card
			#print "stand"
			self.player.ask_limit -= 1
			return False

#draw subclass: if ask limit is less than 5, takes card
class ChanceDraw(Draw):
	def draw(self):
		if self.player.ask_limit < 5:
			#draw
			print "draw"
			self.player.ask_limit += 1
			return True
		else:
			#stand
			print "stand"
			self.player.ask_limit -= 1
			return False

#draw subclass: if win streak is >= 2 then draw
class StreakyDraw(Draw):
	def draw(self):
		if self.player.win_streak >= 2:
			#draw
			print "draw"
			self.player.ask_limit += 1
			return True
		else:
			#stand
			print "stand"
			self.player.ask_limit -= 1
			return False

#draw subclass: strategic draw
#calculate chance of getting winning cards
#if chance > 50%, draw, Strategy.player.ask_limit -= 1
class StrategicDraw(Draw):
	def draw(self):
		#calculate total of player.cards
		print self.calculate_total()
		total = self.calculate_total()
		
		#check which cards to get to win
		needed = 7 - total
		print needed
		
		#calculate chances
		""" need to fix """
		ctr = 4
		for card in self.player.cards:
			if card.number == needed:
				ctr -= 1
		chance = long(ctr)/4.0
		
		#if chance > 50% draw
		if chance > 0.5:
			print "draw"
			self.player.ask_limit += 1
			return True
		else:
			print "stand"
			self.player.ask_limit -= 1
			return False
		
class DealerDraw(Draw):
	def draw(self):
		if self.calculate_total <= 4:
			return True #draw
		else:
			return False #stand
		
class BaccaratDealerDraw(Draw):
	def draw(self):
		if self.player.total >= 0 and self.player.total <= 2:
			return True
		return False
		#more complicated stuff: http://www.gambling-baccarat.com/drawing-rules.htm
	
class BlackjackDealerDraw(Draw):
	def draw(self):
		if self.player.total < 17:
			return True
		return False
		
if __name__ == '__main__':
	player1 = Player("therese")
	player2 = Player("jat")
	player3 = Player("adf")
	
	player1.setCards([Card(6, "hearts"),Card(5, "hearts"),Card(3, "hearts")])
	player2.setCards([Card(2, "hearts"),Card(5, "hearts"),Card(3, "hearts")])
	player3.setCards([11,12,13,14,15])
	
	cards = player2.cards
	
	message = "Drawing menu" \
		+ "\n[1] Random" \
		+ "\n[2] Chance" \
		+ "\n[3] Streaky" \
		+ "\n[4] Strategic" \
		+ "\nEnter: "
	draw_algorithm = raw_input(message)
	
	if draw_algorithm == "1":
		algorithm = RandomDraw(cards)
	elif draw_algorithm == "2":
		algorithm = ChanceDraw(cards)
	elif draw_algorithm == "3":
		algorithm = StreakyDraw(cards)
	elif draw_algorithm == "4":
		algorithm = StrategicDraw(cards)
	else:
		print "Invalid entry"
	
	algorithm.draw()