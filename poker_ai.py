from pokereval.card import Card
from pokereval.hand_evaluator import HandEvaluator

from random import random, shuffle
from multiprocessing import Pool
from time import time
from copy import deepcopy

FULL_DECK = [
		(2, 1),	(3, 1),	(4, 1),	(5, 1), (6, 1), (7, 1),	(8, 1), (9, 1), (10, 1), (11, 1), (12, 1), (13, 1), (14, 1),		
		(2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2), (9, 2), (10, 2), (11, 2), (12, 2), (13, 2), (14, 2),		
		(2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3), (9, 3), (10, 3), (11, 3), (12, 3), (13, 3), (14, 3),		
		(2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4), (9, 4), (10, 4), (11, 4), (12, 4), (13, 4), (14, 4)
	]

# Run monte carlo simulations of a texas hold 'em game
def simulate(num_opponents, hand, community, timeout):
	won = 0
	simulated = 0
	start = time()
	deck = FULL_DECK
	for card in hand:
		deck.remove(card)
	for card in community:
		deck.remove(card)
	
	while time() - start < timeout:
		simulated += 1
		if play_game(num_opponents, hand, community, deck):
			won += 1
	return (won, simulated)

def play_game(num_opponents, hand, community, deck):
	# Shuffle the deck and create a copy of the community cards
	shuffle(deck)
	community_copy = [Card(*c) for c in community]
	
	# Deal cards to each opponent
	opponents = []
	for i in range(num_opponents):
		c1 = deck[i * 2]
		c2 = deck[i * 2 + 1]
		opponents.append([Card(*c1), Card(*c2)])
		
	# Fill up the community cards
	for i in range(5 - len(community)):
		c = deck[num_opponents * 2 + i]
		community_copy.append(Card(*c))
	
	# Score each opponent
	max_opponent = max([HandEvaluator.evaluate_hand(opponent, community_copy) for opponent in opponents])
	
	# Score my hand
	my_hand = [Card(*c) for c in hand]
	my_score = HandEvaluator.evaluate_hand(my_hand, community_copy)

	# Calculate the winner
	if my_score > max_opponent:
		return True
	elif my_score == max_opponent:
		return random() > 0.5
	else:
		return False
			
class PokerAI:
	def __init__(self, numCores = 4, timeout=1):
		self.numCores = numCores
		self.timeout = timeout
		self.blind = 0
		self.lastRound = -1
		
	# A string representing a call decision
	def call_string(self):
		print 'Calling'
		return "action_name=call"
	
	# A string representing a fold decision
	def fold_string(self):
		print 'Folding'
		return "action_name=fold"
	
	# A string representing a bet of <val>
	def bet_string(self, val):
		print 'Betting', val
		return "action_name=bet&amount=" + str(val)
	
	# Simulate games to determine the best course of action
	def make_decision(self, game):
		# Run a monte carlo simulation
		win_prob = self.run_simulation(game)
		bet_amount = self.get_bet_amount(win_prob, game)
		
		# Calculate the current pot odds
		pot_odds = self.calculate_pot_odds(game)
		
		# Find the expected rate of return
		if pot_odds > 0:
			rate_of_return = win_prob / pot_odds
		else:
			rate_of_return = win_prob * 2.3
			
		# Out of money; YOLO
		if game.stack() < 2 * self.blind:
			print 'Out of money.  Going all in.'
			return self.bet_string(game.stack())
			
		# Almost certain win; YOLO
		if win_prob > 0.95:
			print "We basically can't lose..."
			return self.bet_string(game.stack())
		
		# Make a decision based on our rate of return
		val = random()
		if rate_of_return < 0.8:
			if val < 0.95 and game.call_amount() > 0:
				return self.fold_string()
			else:
				return self.bet_string(bet_amount)
		elif rate_of_return < 1.0:
			if val < 0.8 and game.call_amount()  > 0:
				return self.fold_string()
			elif val < 0.85:
				return self.call_string()
			else:
				return self.bet_string(bet_amount)
		elif rate_of_return < 1.3:
			if val < 0.6:
				return self.call_string()
			else:
				return self.bet_string(bet_amount)
		else:
			if val < 0.3:
				return self.call_string()
			else:
				return self.bet_string(bet_amount)
	
	def get_bet_amount(self, win_prob, game):
		return int(win_prob * game.stack())
		
	# Run a parallel monte carlo simulation
	def run_simulation(self, game):
		# Get relevant information for the simulation
		num_opponents = game.still_playing()
		hand = game.hand()
		community = game.community()
		
		# Create the process pool
		pool = Pool(self.numCores)
		won = 0
		simulated = 0
		args = (num_opponents, hand, community, self.timeout)
		
		# Spawn the processes
		results = []
		for _ in range(self.numCores):
			results.append(pool.apply_async(simulate, args))
		
		# Wait for the threads to return
		pool.close()
		pool.join()
		
		# Accumulate results
		for result in results:
			result = result.get()
			won += result[0]
			simulated += result[1]
		
		# Print the number of simulations run and return
		win_prob = float(won) / simulated
		print 'Number of simulations:\t', simulated
		print 'Win probability:\t', win_prob
		return win_prob
	
	# Calculate the pot odds of this hand
	def calculate_pot_odds(self, game):
		# Get the latest blind value
		if game.roundID() != self.lastRound:
			self.lastRound = game.roundID()
			self.blind = game.call_amount()
		
		call = game.call_amount()
		current = game.current_bet()
		if call + current > 0:
			return float(call) / (call + current)
