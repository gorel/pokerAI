import json

class GameState:
	PHASES = {
		'deal'  : 1,
		'flop'  : 2,
		'turn'  : 3,
		'river' : 4,
	}
	
	CARDS = {
		'2S' : (2, 1),
		'3S' : (3, 1),
		'4S' : (4, 1),
		'5S' : (5, 1),
		'6S' : (6, 1),
		'7S' : (7, 1),
		'8S' : (8, 1),
		'9S' : (9, 1),
		'TS' : (10, 1),
		'JS' : (11, 1),
		'QS' : (12, 1),
		'KS' : (13, 1),
		'AS' : (14, 1),
		
		'2H' : (2, 2),
		'3H' : (3, 2),
		'4H' : (4, 2),
		'5H' : (5, 2),
		'6H' : (6, 2),
		'7H' : (7, 2),
		'8H' : (8, 2),
		'9H' : (9, 2),
		'TH' : (10, 2),
		'JH' : (11, 2),
		'QH' : (12, 2),
		'KH' : (13, 2),
		'AH' : (14, 2),
		
		'2D' : (2, 3),
		'3D' : (3, 3),
		'4D' : (4, 3),
		'5D' : (5, 3),
		'6D' : (6, 3),
		'7D' : (7, 3),
		'8D' : (8, 3),
		'9D' : (9, 3),
		'TD' : (10, 3),
		'JD' : (11, 3),
		'QD' : (12, 3),
		'KD' : (13, 3),
		'AD' : (14, 3),
		
		'2C' : (2, 4),
		'3C' : (3, 4),
		'4C' : (4, 4),
		'5C' : (5, 4),
		'6C' : (6, 4),
		'7C' : (7, 4),
		'8C' : (8, 4),
		'9C' : (9, 4),
		'TC' : (10, 4),
		'JC' : (11, 4),
		'QC' : (12, 4),
		'KC' : (13, 4),
		'AC' : (14, 4)
	}

	def __init__(self, jsonString):
		try:
			self.jsonVals = json.loads(jsonString)
			self.players = self.jsonVals['players_at_table']
		except:
			print 'Could not parse json'
			return None
	
	# Returns whether or not it is our turn
	def my_turn(self):
		return self.jsonVals['your_turn']
		
	# Returns the stack we had at the beginning of this round
	def initialStack(self):
		return self.jsonVals['initial_stack']
	
	# Returns the current stack we have
	def stack(self):
		return self.jsonVals['stack']
	
	# Returns the current bet on the table
	def current_bet(self):
		return self.jsonVals['current_bet']
	
	# Returns the amount we would have to play to call
	def call_amount(self):
		return self.jsonVals['call_amount']
	
	# Returns the round id of the game
	def roundID(self):
		return self.jsonVals['round_id']
	
	# Returns an integer representation of the phase of the game
	def phase(self):
		game_phase = self.jsonVals['betting_phase']
		return self.PHASES[game_phase]
	
	# Returns an array of the players at the table
	def players(self):
		return self.players
	
	# Returns the number of players still playing the game
	def still_playing(self):
		return len(self.players)
	
	# Returns a mapping of my hand of cards
	def hand(self):
		hand = []
		for card in self.jsonVals['hand']:
			hand.append(self.CARDS[card])
		return hand
	
	# Returns a mapping of the community cards currently in play
	def community(self):
		community = []
		for card in self.jsonVals['community_cards']:
			community.append(self.CARDS[card])
		return community
	
