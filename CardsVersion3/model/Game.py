from Card import *
from Player import *
from ShufflingAlgorithms import *
from Observer import Subject
from DrawingAlgorithms import *

class Game(object):
	max_players = 6
	min_players = 1
	
	def __init__(self):
		self.players = []
		self.deck = []
		self.curplayer = None
		self.make_observer_list()
		
	def add_player(self, new_player):
		num_of_players = len(self.players)
		if (num_of_players > Game.max_players):
			raise Exception #game is full
		else:
			self.players.append(new_player)
			new_player.enter_game(self.get_card)
			self.register_observer(new_player.update_curplayer)
			
	def remove_player(self, player):
		self.players.remove(player)
		'''should it be update_curplayer?'''
		self.remove_observer(player.update_curplayer)
	
	def check_game_initial_state(self):
		num_of_players = len(self.players)
		if (num_of_players < Game.min_players):
			#raise Exception #not enough players
			return False
		for player in self.players:
			if not player.isReady():
				self.players.remove(player)
				print "removed " + player.name + " from game"
		self.dealer.isReady()
		return True
	
	def get_card(self):
		return self.deck.pop(0)
	
	def set_shuffle_algorithm(self, algorithm_str):
		if algorithm_str == "random":
			self.shuffle_algorithm = RandomShuffle(self.deck)
		elif algorithm_str == "cutandmerge":
			repititions = int(raw_input("Enter number of times to cut and merge > "))
			self.shuffle_algorithm = CutAndMergeShuffle(self.deck, repititions)
		elif algorithm_str == "divideandover":
			repititions = int(raw_input("Enter number of times to cut and merge > "))
			self.shuffle_algorithm = DivideAndOverShuffle(self.deck, repititions)
		else:
			print "Invalid entry"
			
	def shuffle_deck(self):
		self.shuffle_algorithm.set_cards(self.deck)
		self.deck = self.shuffle_algorithm.shuffle()
		
	#deal to all players including dealer
	def deal_to_all(self):
		for player in self.players:
			card = self.get_card()
			player.receive_card(card)
			
		card = self.get_card()
		self.dealer.receive_card(card)
		
	def ask_for_third_card(self, player):
		player.draw()
		
	def start_game(self):
		print 'starting a '+self.name+' game....'
		ready_to_play = self.check_game_initial_state()
		if ready_to_play:
			#shuffle deck
			self.shuffle_deck()
			#deal 2 cards for each player and dealer
			print 'dealing 1st card...'
			self.deal_to_all()
			print 'dealing 2nd card...'
			self.deal_to_all()
			print 'end of dealing...'
			print 'start of drawing third card..'
			#players stands or hits for third card
			self.do_round_of_drawing_cards()
			print 'start of paying bets...'
			#dealer pays bets from left to right
			for player in self.players:
				self.check_for_winnings(player)
			self.end_game()
		else:
			print "not ready to play: not enough players or players have not placed bet"
	
	def do_round_of_drawing_cards(self):
		for player in self.players:
			self._set_curplayer(player)
			self.ask_for_third_card(player)
		self.ask_for_third_card(self.dealer)
	
	def _set_curplayer(self, player):
		self.curplayer = player
		self.notify_observers(self.curplayer)#that dealer is tied and its first player's turn
		
	def end_game(self):
		print 'ending game..'
		#ask if new game?
		pass
	
class Blackjack(Game, Subject):
	name = "Blackjack"
	max_players = 6
	min_players = 1
	tie_winnings = 0 #if dealer and player have same value, push
	winnings = 1.5 #blackjack pays 3 to 2
	
	def __init__(self):
		super(Blackjack, self).__init__()
		self.dealer = PlayerFactory.createPlayer("blackjackdealer", None)
		self.deck = CardFactory.createDeck(2, Blackjack.name)
		#add dealer to game
		self.dealer.enter_game(self.get_card)
		self.register_observer(self.dealer.update_curplayer)
		
	def check_for_winnings(self, player):
		#check for tie
		if player.total == self.dealer.total:
			print player.name, "push, player tied with dealer "
		else:
			#21 points on the player's first two cards, without a dealer blackjack
			if player.total == 21 and self.dealer.total != 21:
				winnings = player.pay(player.bet)*Blackjack.winnings
				player.win_money(winnings)
				print player.name, "won blackjack, 21 " + str(winnings)
			#score higher than the dealer without exceeding 21
			elif player.total <= 21 and player.total > self.dealer.total:
				winnings = player.pay(player.bet)*Blackjack.winnings
				player.win_money(winnings)
				print player.name, "won blackjack, more than dealer " + str(winnings)
			else:
				#player lose bets
				player.pay(player.bet)
				print player.name, "loses bet"
	
	
class Baccarat(Game, Subject):
	name = "Baccarat"
	player_bet_winnings = 1#pays 1 to 1
	banker_bet_winnings = 1#pays 1 to 1
	tie_bet_winnings = 8#pays 8 to 1
	
	def __init__(self):
		super(Baccarat, self).__init__()
		self.dealer = PlayerFactory.createPlayer("baccaratdealer", None)
		self.deck = CardFactory.createDeck(2, Baccarat.name)
		#add dealer to game
		self.dealer.enter_game(self.get_card)
		self.register_observer(self.dealer.update_curplayer)
		
	def check_for_winnings(self, player):
		#check for tie
		if player.tie_bet != 0:
			if player.total == self.dealer.total:
				print player.name, "push, tied with dealer"
			else:
				player.pay(player.tie_bet)
				print player.name, "loses tie bet"
		#banker bet: banker wins
		if player.banker_bet != 0:
			if player.total < self.dealer.total:
				winnings = player.pay(player.banker_bet)*Baccarat.banker_bet_winnings
				player.win_money(winnings)
				print player.name, "banker won, " + str(winnings)
			else:
				player.pay(player.banker_bet)
				print player.name, "loses banker bet"
		#player bet: player wins
		if player.player_bet != 0:
			if player.total > self.dealer.total:
				winnings = player.pay(player.player_bet)*Baccarat.player_bet_winnings
				player.win_money(winnings)
				print player.name, "player won, " + str(winnings) 
			else:
				player.pay(player.player_bet)
				print player.name, "loses player bet"
			
	
	
	
	
class Lucky9(Game, Subject):
	name = "Lucky9"
	tie_winnings = 7 #pays 7:1
	lucky9_winnings = 1.5 #pays 3:2
	max_players = 6
	min_players = 1
	
	def __init__(self):
		super(Lucky9, self).__init__()
		self.dealer = PlayerFactory.createPlayer("lucky9dealer", None)
		self.deck = CardFactory.createDeck(2, Lucky9.name)
		#add dealer to game
		self.dealer.enter_game(self.get_card)
		self.register_observer(self.dealer.update_curplayer)
	
	def start_game(self):
		#check if there is enough players and all players have placed bet
		print 'starting a '+self.name+' game....'
		ready_to_play = self.check_game_initial_state()
		if ready_to_play:
			#shuffle deck
			self.shuffle_deck()
			#deal 2 cards for each player and dealer
			print 'dealing 1st card...'
			self.deal_to_all()
			print 'dealing 2nd card...'
			self.deal_to_all()
			print 'end of dealing...'
			#pay lucky9 bonus winners
			print 'paying bonus winners...'
			self.pay_lucky9_bonus_winners()
			#players from left to right draw cards
			print 'players may get third card...'
			self.do_round_of_drawing_cards()
			print 'end of playing...'
			print 'dealer reveals up card...'
			print self.dealer.upcard
			print 'dealer draws or stands...'
			self._set_curplayer(self.dealer)
			print dealer
			print 'dealer pays tie and wager bets...'
			#dealer pays bets from right to left
			for player in reversed(self.players):
				self.check_for_winnings(player)
			self.end_game()
			""" TODO(CHECK FOR LOGIC), LOGIC BEHIND TOTAL MAYBE WRONG """
			for player in reversed(self.players):
				self.check_for_winnings(player)
		else:
			print "not ready to play: not enough players or players have not placed bet"
					
	def check_for_winnings(self, player):
		#check for tie
		if player.total == self.dealer.total and self.dealer.total != 9:
			winnings = player.pay(player.tie_bet)*Lucky9.tie_winnings
			player.win_money(winnings)
			print player.name, "won tie " + str(winnings)
		#check if lucky 9
		elif player.total == 9 and self.dealer.total != 9:
			winnings = player.pay(player.lucky9_wager)*Lucky9.lucky9_winnings
			player.win_money(winnings)
			print player.name, "won lucky9 " + str(winnings)
		elif player.total == 9 and self.dealer.total == 9:
			#player does not pay or lose money (even money)
			print player.name, "push, even money"
		else:
			#player lose bets
			player.pay(player.tie_bet)
			player.pay(player.lucky9_wager)
			print player.name, "loses bet"
	
	def calculate_total(self, cards):
		value_list = [card.value for card in cards]
		self.total = sum(value_list)
		return self.total #total is (sum of all values)
	
	def get_lucky9_bonus(self, cards, bet):
		#suited 3-3-3 pays 200 to 1
		#suited 2-3-4 pays 100 to 1
		if all(card.value == 3 for card in cards):
			return bet*50 #pays 50 to 1
		#any 3-3-3 pays 50 to 1
		#any 2-3-4 pays 40 to 1
		#suited 9 pays 30 to 1
		elif self.calculate_total(cards) == 9:
			return bet*5 #total 9 pays 5 to 1
		else:
			return 0
	
	def pay_lucky9_bonus_winners(self):
		#wins bonus_bet, if first two cards + dealer upcard = 9
		for player in self.players:
			if player.bonus_bet != 0:
				cards = player.cards[1:2] + [dealer.upcard]
				if self.calculate_total(cards) == 9:
					winnings = self.get_lucky9_bonus(cards, player.bonus_bet)
					if winnings == 0:
						print player.name, "lost lucky bonus"
					else:
						print player.name, "won lucky bonus ", str(winnings)
						player.add_money(winnings)

		if all(player.bonus_bet == 0 for player in self.players):
			print "<no lucky bonus bets placed>"
	
	#pay player if lucky 9 total with 2 cards
	def pay_lucky9_winner(self, player):
		if len(player.cards) <= 2:
			raise Exception #should only pay when first 2 cards total 9
		elif player.calculate_total() != 9:
			raise Exception #total should be 9
		else:
			#player.pay_money(self.)
			pass
		
class GameFactory(object):
	@staticmethod
	def createGame(type):
		if type == Lucky9.name: return Lucky9()
		if type == Blackjack.name: return Blackjack()
		if type == Baccarat.name: return Baccarat()
		assert 0, "Bad game creation: " + type
	
if __name__ == '__main__':
	
	#test for lucky 9
	player1 = PlayerFactory.createPlayer("lucky9player", "a")
	player1.set_draw_strategy(ChanceDraw(player1))
	player2 = PlayerFactory.createPlayer("lucky9player", "b")
	player2.set_draw_strategy(StreakyDraw(player2))
	player3 = PlayerFactory.createPlayer("lucky9player", "c")
	player3.set_draw_strategy(RandomDraw(player3))
	player4 = PlayerFactory.createPlayer("lucky9player", "d")
	player4.set_draw_strategy(RandomDraw(player4))
	player5 = PlayerFactory.createPlayer("lucky9player", "e")
	player5.set_draw_strategy(StrategicDraw(player5))
	player6 = PlayerFactory.createPlayer("lucky9player", "f")
	player6.set_draw_strategy(StreakyDraw(player6))
	
	game = GameFactory.createGame("Lucky9")
	'''
	game.add_player(player1)
	game.add_player(player2)
	game.add_player(player3)
	game.add_player(player4)
	game.add_player(player5)
	game.add_player(player6)
	
	dealer = game.dealer
	
	for _ in range(2):
		for player in game.players:
			player.lucky9_wager = 50
			player.bonus_bet = 50
			player.tie_bet = 20

		game.set_shuffle_algorithm("random")
		game.start_game()

		for player in game.players: print player
		print dealer
		
	for player in game.players: print player.name, ":[", player.winning_streak, "]", 
	
	
	player1 = PlayerFactory.createPlayer("blackjackplayer", "a")
	player2 = PlayerFactory.createPlayer("blackjackplayer", "b")
	player3 = PlayerFactory.createPlayer("blackjackplayer", "c")
	player4 = PlayerFactory.createPlayer("blackjackplayer", "d")
	player5 = PlayerFactory.createPlayer("blackjackplayer", "e")
	player6 = PlayerFactory.createPlayer("blackjackplayer", "f")
	
	game = GameFactory.createGame("Blackjack")
	
	
	player1 = PlayerFactory.createPlayer("baccaratplayer", "a")
	player1.set_draw_strategy(ChanceDraw(player1))
	player2 = PlayerFactory.createPlayer("baccaratplayer", "b")
	player2.set_draw_strategy(StreakyDraw(player2))
	player3 = PlayerFactory.createPlayer("baccaratplayer", "c")
	player3.set_draw_strategy(RandomDraw(player3))
	player4 = PlayerFactory.createPlayer("baccaratplayer", "d")
	player4.set_draw_strategy(RandomDraw(player4))
	player5 = PlayerFactory.createPlayer("baccaratplayer", "e")
	player5.set_draw_strategy(StrategicDraw(player5))
	player6 = PlayerFactory.createPlayer("baccaratplayer", "f")
	player6.set_draw_strategy(StreakyDraw(player6))
	
	game = GameFactory.createGame("Baccarat")
	'''
	game.add_player(player1)
	game.add_player(player2)
	game.add_player(player3)
	game.add_player(player4)
	game.add_player(player5)
	game.add_player(player6)
	dealer = game.dealer
	
	for _ in range(2):
		for player in game.players:
			player.lucky9_wager = 50
			player.bonus_bet = 50
			player.tie_bet = 20

		game.set_shuffle_algorithm("random")
		game.start_game()

		for player in game.players: print player
		print dealer
	