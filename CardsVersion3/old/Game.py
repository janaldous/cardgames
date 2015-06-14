from Card import *
from Player import *
from ShufflingAlgorithms import *
from Observer import Subject

class Lucky9(Subject):
	tie_winnings = 7 #pays 7:1
	lucky9_winnings = 1.5 #pays 3:2
	max_players = 6
	min_players = 1
	
	def __init__(self):
		self.name = "Lucky9"
		self.deck = CardFactory.createDeck()
		self.players = []
		self.curplayer = None
		self.dealer = PlayerFactory.createPlayer("lucky9dealer", None)
		self.make_observer_list()
	
	def add_player(self, new_player):
		if (len(self.players) > Lucky9.max_players):
			raise Exception #game is full
		else:
			self.players.append(new_player)
			new_player.enter_game(self.get_card)
			self.register_observer(new_player.update_curplayer)
			
	def remove_player(self, player):
		self.players.remove(player)
		self.remove_observer(player.update_curplayer)
		
	def start_game(self):
		print 'starting game...'
		if (len(self.players) < Lucky9.min_players):
			raise Exception #not enough players
		for player in self.players:
			if player.bet == 0:
				raise Exception #not all players have placed a bet
			elif player.isPlaying == False:
				self.players.remove(player)
				print "removed " + player.name + " from game"
		else:
			#add dealer to game
			self.dealer.enter_game(self.get_card)
			self.register_observer(self.dealer.update_curplayer)
			#shuffle deck
			self.shuffle_deck()
			#deal 2 cards for each player and dealer
			self.deal_to_all()
			self.deal_to_all()
			
			if not self.dealer.hasNatural9():
				#condition1: if dealer does not have natural, and some players have natural, pay winners, end game
				condition1_flag = False
				winners = []
				for player in self.players:
					if player.hasNatural9():
						winners.append(player)
						condition1_flag = True
				
				#for condition1
				if condition1_flag == True:
					print 'natural players win!'
					self.collect_bets_pay_winners(winners)
					#self.notify_observers()#that game has ended
					self.end_game()
				#condition2: if both dealer and all players do not have naturals, tie, game continues
				else:
					for player in self.players:
						if not player.hasNatural9():
							player.at_tie()
							dealer.isTied = True#at_tie()
							print 'tie1' + player.name
				
			else:
				#condition3: if dealer has natural and no other players have natural, collect bets, end game
				for player in self.players:
					if player.hasNatural9():
						pass
				else:
					print 'dealer wins!'
					self.collect_all_bets()
					#self.notify_observers()#that game has ended
					self.end_game()
				#condition4: if dealer has natural and some players have natural, tie, pays back bets to winners, end game
				for player in self.players:
					if player.hasNatural9():
						player.at_tie()
						dealer.at_tie()
						print 'tie2'
			
			print 'end of dealing...'
				
			if dealer.isTied == True:
				print 'tie game..'
				#pick first player
				self.round_of_drawing_cards()
				winners = [player for player in self.players if player.hasNatural9()]
				self.collect_bets_pay_tie_winners(winners);
				self.end_game()
			
	def round_of_drawing_cards(self):
		for player in self.players:
			self.set_curplayer(player)
			raw_input("Ok? ")
			
		self.set_curplayer(self.dealer)
	
	def set_curplayer(self, player):
		self.curplayer = player
		self.notify_observers(self.curplayer)#that dealer is tied and its first player's turn
			
	def end_game(self):
		print 'ending game..'
		#pay winners
		#ask if new game?
		pass
	
	def collect_bets_pay_tie_winners(self, winners):
		for player in self.players:
			for winner in winners:
				if player != winner:
					player.pay(player.bet)
				else:
					winnings = player.pay(player.bet)*Lucky9.tie_winnings
					player.add_money(winnings)
					print str(player) + " won " + str(winnings)
	
	def collect_all_bets(self):
		print "collecting bets..."
		for player in self.players:
			player.pay(player.bet)
			
	def collect_bets_pay_winners(self, winners):
		for player in self.players:
			for winner in winners:
				if player != winner:
					player.pay(player.bet)
				else:
					winnings = player.pay(player.bet)*Lucky9.lucky9_winnings
					player.add_money(winnings)
					print str(player) + " won " + str(winnings)
				
	def set_shuffle_algorithm(self, algorithm):
		if algorithm == "random":
			self.shuffle_algorithm = RandomShuffle(self.deck)
		elif algorithm == "cutandmerge":
			repititions = int(raw_input("Enter number of times to cut and merge > "))
			self.shuffle_algorithm = CutAndMergeShuffle(self.deck, repititions)
		elif algorithm == "divideandover":
			repititions = int(raw_input("Enter number of times to cut and merge > "))
			self.shuffle_algorithm = DivideAndOverShuffle(self.deck, repititions)
		else:
			print "Invalid entry"
	
	def shuffle_deck(self):
		self.shuffle_algorithm.set_cards(self.deck)
		self.deck = self.shuffle_algorithm.shuffle()
		
	def get_card(self):
		return self.deck.pop(0)
	
	def pass_turn(self):
		pass
		
	#deal to all players including dealer
	def deal_to_all(self):
		for player in self.players:
			player.receive_card(self.get_card())
		self.dealer.receive_card(self.get_card())
	
	#pay player if ties with dealer
	def pay_tie_winner(self, player):
		pass
	
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
		if type == "lucky9": return Lucky9()
		assert 0, "Bad game creation: " + type
	
if __name__ == '__main__':
	player1 = PlayerFactory.createPlayer("player", "a")
	player2 = PlayerFactory.createPlayer("player", "b")
	player3 = PlayerFactory.createPlayer("player", "c")
	player4 = PlayerFactory.createPlayer("player", "d")
	player5 = PlayerFactory.createPlayer("player", "e")
	player6 = PlayerFactory.createPlayer("player", "f")
	
	game = GameFactory.createGame("lucky9")
	game.add_player(player1)
	game.add_player(player2)
	game.add_player(player3)
	game.add_player(player4)
	game.add_player(player5)
	game.add_player(player6)
	dealer = game.dealer
	
	for _ in range(1):
		for player in game.players:
			player.place_bet()

		game.set_shuffle_algorithm("random")
		game.start_game()

		for player in game.players: print player
		print dealer
		
	for player in game.players: print player.name, player.winning_streak