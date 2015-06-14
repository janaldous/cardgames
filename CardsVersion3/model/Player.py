from Observer import *
from DrawingAlgorithms import *

class Player(Observer):
	playerCounter = 0 #static variable
	winning_streak = 0
	ask_limit = 0
		
	def __init__(self, name):
		self.name = name
		self.cards = []
		self.total = 0
		self.money = 200
		self.isCurplayer = False
		self.isPlaying = False
		Player.playerCounter += 1 #static variable
		self.playerNumber = Player.playerCounter
		
	def set_name(self, name):
		self.name = name
		
	def add_money(self, additional):
		self.money += additional
		
	def win_money(self, winnings):
		self.money += winnings
		self.winning_streak += 1
		
	def pay(self, bet):
		self.bet = 0
		self.money -= bet
		self.winning_streak = 0
		return bet
		
	def enter_game(self, get_card_method):
		self.isPlaying = True
		self.cards = []
		self.set_draw_strategy(RandomDraw(self))
		self.game_get_card = get_card_method
		
	def update_turn(self):
		self.draw()
		
	def exit_game(self):
		self.isPlaying = False
		
	def at_tie(self):
		self.isTie = True
		
	def calculate_total(self):
		total = 0
		for card in self.cards:
			total += card.value
		self.total = total
		return total % 10
		
	def draw(self):
		if self.draw_strategy.draw() == True:
			#hit
			self.receive_card(self.game_get_card())
			return True
		else:
			#stand
			print self.name + ' stands'
			return False
		
	def receive_card(self, card):
		self.cards.append(card)
		#calculate total
		self.total = self.calculate_total()
		print self.name + ' gets ' + str(card)
	
	def set_cards(self, cards):
		self.cards = cards
	
	def set_draw_strategy(self, draw_strategy):
		self.draw_strategy = draw_strategy
		
	def calculate_chance_of_winning(self):
		pass
	
	def hasNatural9(self):
		#cannot be 10 or above
		for card in self.cards:
			if card.number >= 10:
				return False
		if len(self.cards) == 2 and self.calculate_total() == 9:
			return True
		else:
			return False
		
	def update_curplayer(self, observer):
		if self == observer:
			self.isCurplayer = True
			self.draw()
		else:
			self.isCurplayer = False
			
	def isReady(self):
		#player has nothing in his hand
		self.cards = []
		#has bet and has enough money
		if self.hasBet() and self.money-self.get_total_bet() > 0:
			print self.name, 'is ready'
			return True
		return False
	
	def start_game(self):
		self.cards = []
		self.total = 0
		self.isCurplayer = False
		self.isPlaying = False
		
	def hasBet(self):
		return True
	
	def __str__(self):
		str_cards = ", ".join(str(card) for card in self.cards)
		return "[Player " + str(self.playerNumber) +  ": " + self.name + "] " + str_cards + " " \
			+ str(self.total) + " $" + str(self.money)

class Dealer(Player):
	def __init__(self):
		self.name = "dealer"
		self.cards = []
		self.isCurplayer = False
		self.isTied = False
		self.total = 0
		self.set_draw_strategy(DealerDraw(self.cards))
		self.money = 1#filler value to reuse method isReady()
		
	def receive_card(self, card):
		self.cards.append(card)	
		self.total = self.calculate_total()
	
	def __str__(self):
		str_cards = ", ".join(str(card) for card in self.cards)
		return "[Dealer : " + self.name + "] " + str_cards + " " + str(self.total)
	

	
class UserPlayer(Player):
	def place_bet(self, bet):
		if (self.money - bet) < 0:
			return False
			raise Exception #not enough money
		else:
			self.bet = bet
			return True
		
	def draw(self):
		#ask user
		user_input = input("Draw? (y/n)")
		if user_input.lowercase == "y":
			#draw
			pass
		elif user_input.lowercase == "n":
			#dont draw
			pass
		else:
			print "invalid input"
	
	def isReady(self):
		#has bet, has enough money, asks player if willing to play
		pass

class Lucky9Player(Player):
	def __init__(self, name):
		Player.__init__(self, name)
		self.tie_bet = 0#players cards total = dealer cards total
		self.bonus_bet = 0 #first two cards + dealers upcard is 9
		self.lucky9_wager = 0#
		
	def calculate_total(self):
		value_list = [card.value for card in self.cards]
		self.total = sum(value_list)
		return self.total%10 #total is (sum of all values)
	
	def hasBet(self):
		if self.tie_bet > 0 or self.bonus_bet > 0  or self.lucky9_wager > 0:
			return True
		return False
	
	def get_total_bet(self):
		return self.tie_bet + self.bonus_bet + self.lucky9_wager
	
class Lucky9Dealer(Lucky9Player, Dealer):
	def __init__(self, name='dealer'):
		Lucky9Player.__init__(self, name)
		
	def receive_card(self, card):
		self.cards.append(card)
		if (len(self.cards) == 1):
			self.downcard = card
		elif (len(self.cards) == 2):
			self.upcard = card
		self.total = self.calculate_total()
	
class BlackjackPlayer(Player):
	def __init__(self, name):
		Player.__init__(self, name)
		self.bet = 0
	
	def calculate_total(self):
		value_list = [card.value for card in self.cards]
		self.total = sum(value_list)
		return self.total #total is (sum of all values)
	
	def hasBet(self):
		#blackjack only has 2 bets
		if self.bet > 0 or self.tie_bet > 0:
			return True
		return False
	
class BlackjackDealer(BlackjackPlayer):
	def __init__(self, name='dealer'):
		BlackjackPlayer.__init__(self, name)
		self.set_draw_strategy(BlackjackDealerDraw(self))
	
class BaccaratPlayer(BlackjackPlayer):
	def __init__(self, name):
		BlackjackPlayer.__init__(self, name)
		self.player_bet = 0
		self.banker_bet = 0
		self.tie_bet = 0
		
	def calculate_total(self):
		value_list = [card.value for card in self.cards]
		self.total = sum(value_list)
		return self.total%10 #total is (sum of all values)
		
	def hasBet(self):
		if self.player_bet > 0 or self.banker_bet > 0  or self.tie_bet > 0:
			return True
		return False

class BaccaratDealer(BaccaratPlayer):
	def __init__(self, name='dealer'):
		BaccaratPlayer.__init__(self, name)
		self.set_draw_strategy(BaccaratDealerDraw(self))
	
class PlayerFactory(object):
	def createPlayer(type, name):
		if type == "player": return Player(name)
		if type == "dealer": return Dealer()
		if type == "banker": return Dealer()
		if type == "lucky9player": return Lucky9Player(name)
		if type == "lucky9dealer": return Lucky9Dealer()
		if type == "lucky9user": return UserPlayer(name)
		if type == "blackjackplayer": return BlackjackPlayer(name)
		if type == "blackjackuser": return BlackjackPlayer(name)
		if type == "blackjackdealer": return BlackjackDealer()
		if type == "baccaratplayer": return BaccaratPlayer(name)
		if type == "baccaratdealer": return BaccaratDealer()
		assert 0, "Bad player creation: " + type
	createPlayer = staticmethod(createPlayer)
	
if __name__ == '__main__':
	player1 = Player("therese")
	player2 = Player("jat")
	player3 = Player("adf")
	
	print player1, player2, player3
	
	playerFactory = PlayerFactory()
	player1 = playerFactory.createPlayer("player", "jat")
	player2 = playerFactory.createPlayer("player", "therese")
	dealer = playerFactory.createPlayer("lucky9dealer", None)
	
	print player1, player2, drawer