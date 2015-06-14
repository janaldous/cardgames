import math
from Game import *

class Card(object):
	suits = ["hearts", "diamonds", "spades", "clubs"]
	
	def __init__(self, number, suit):
		#validation
		if number > 14 and number < 1:
			raise TypeError #number does not exist
		if suit not in Card.suits:
			raise TypeError #suit does not exist
		
		self.suit = suit
		self.value = number
		
		if number == 1:
			self.n_name = "ace"
		elif number == 11:
			self.n_name = "jack"
		elif number == 12:
			self.n_name = "queen"
		elif number == 13:
			self.n_name = "king"
		else:
			self.n_name = str(number)

	def __str__(self):
		return "[" + self.n_name + " of " + self.suit + "]"
	
	def create_deck(num_of_decks):
		deck = []
		for _ in range(num_of_decks):
			for suit in Card.suits:
				for i in range(1, 14):
					card = Card(i, suit)
					deck.append(card)
		return deck
	create_deck = staticmethod(create_deck)
	
class BlackjackCard(Card):
	def __init__(self, number, suit):
		#validation
		if number > 14 and number < 1:
			raise TypeError #number does not exist
		if suit not in Card.suits:
			raise TypeError #suit does not exist
		
		self.suit = suit
		self.value = number
		
		if number == 1:
			self.n_name = "ace"
		elif number == 11:
			self.n_name = "jack"
			self.value = 10
		elif number == 12:
			self.n_name = "queen"
			self.value = 10
		elif number == 13:
			self.n_name = "king"
			self.value = 10
		else:
			self.n_name = str(number)
		
	def create_deck(num_of_decks):
		deck = []
		for _ in range(num_of_decks):
			for suit in Card.suits:
				for i in range(1, 14):
					card = BlackjackCard(i, suit)
					deck.append(card)
		return deck
	create_deck = staticmethod(create_deck)
	
class BaccaratCard(Card):
	def __init__(self, number, suit):
		#validation
		if number > 14 and number < 1:
			raise TypeError #number does not exist
		if suit not in Card.suits:
			raise TypeError #suit does not exist
		
		self.suit = suit
		
		self.n_name = str(number)
		if number == 1:
			self.n_name = "ace"
			self.value = 1
		elif number == 10:
			self.value = 0
		elif number == 11:
			self.n_name = "jack"
			self.value = 0
		elif number == 12:
			self.n_name = "queen"
			self.value = 0
		elif number == 13:
			self.n_name = "king"
			self.value = 0
		else:
			self.n_name = str(number)
			self.value = number
	
	
class CardFactory(object):
	def createCard(number, type):
		if type == "hearts": return Card(number, "hearts")
		if type == "diamonds": return Card(number, "diamonds")
		if type == "spades": return Card(number, "spades")
		if type == "clubs": return Card(number, "clubs")
		assert 0, "Bad card creation: " + type
	createCard = staticmethod(createCard)
	
	def createDeck(num_of_decks, type):
		if type == Lucky9.name: return Card.create_deck(num_of_decks)
		if type == Blackjack.name: return BlackjackCard.create_deck(num_of_decks)
		if type == Baccarat.name: return BaccaratCard.create_deck(num_of_decks)
	createDeck = staticmethod(createDeck)
	
if __name__ == '__main__':
	card1 = Card("ace", "hearts")
	card2 = Card(2, "hearts")
	card3 = Card(3, "hearts")
	card4 = Card(4, "hearts")
	card5 = Card(5, "hearts")
	card6 = Card(6, "hearts")
	card7 = Card("king", "hearts")
	
	print card1, card2, card3, card4, card5, card6, card7
	
	suits = ["hearts", "diamonds", "spades", "clubs"]
	deck = []
	for suit in suits:
		for i in range(1, 14):
			card = CardFactory.createCard(i, suit)
			deck.append(card)
	
	for card in deck:
		print card