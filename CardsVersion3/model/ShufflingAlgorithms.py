import random
#///////////////////////// SHUFFLING: design pattern: STRATEGY //////////////////////////////
#Super class
class Shuffle(object):
	def __init__(self, cards):
		self.cards = cards

	def set_cards(self, cards):
		self.cards = cards
		
	def shuffle(self):
		pass

#Sub class: randomly shuffles using built in python shuffle method
class RandomShuffle(Shuffle):
	def shuffle(self):
		random.shuffle(self.cards)
		return self.cards

#Sub class: cuts deck in half and merges them one after another
class CutAndMergeShuffle(Shuffle):
	def __init__(self, cards, repititions):
		self.cards = cards
		self.repititions = repititions
	
	def shuffle(self):
		final_order = self.cards
		for _ in range(repititions):
			deck1 = final_order[0: 26]
			deck2 = final_order[26: 52]
			final_order = []
			for i in range(26):
				final_order.append(deck1[i])
				final_order.append(deck2[i])
		return final_order

#Sub class: divide deck into 3 divisions and shuffles them
class DivideAndOverShuffle(Shuffle):
	def __init__(self, cards, repititions):
		self.cards = cards
		self.repititions = repititions
	
	def shuffle(self):
		#third = len(cards)/3
		final_order = self.cards
		for _ in range(repititions):
			deck1 = final_order[0: 17]
			deck2 = final_order[17: 34]
			deck3 = final_order[34: 52]
			final_order = deck3 + deck1 + deck2
		return final_order

#main method
if __name__ == '__main__':
	cards = []
	for i in range(52): 
		cards.append(i+1)
	#print cards

	message = "Shuffle menu" + "\n[1] Random" + "\n[2] Cut and merge" + "\n[3] Divide and over" + "\nEnter: "
	shuffle_algorithm = raw_input(message)
	
	if shuffle_algorithm == "1":
		algorithm = RandomShuffle(cards)
	elif shuffle_algorithm == "2":
		repititions = int(raw_input("Enter number of times to cut and merge > "))
		algorithm = CutAndMergeShuffle(cards, repititions)
	elif shuffle_algorithm == "3":
		repititions = int(raw_input("Enter number of times to cut and merge > "))
		algorithm = DivideAndOverShuffle(cards, repititions)
	else:
		print "Invalid entry"
	
	print "final sequence:"
	print algorithm.shuffle()