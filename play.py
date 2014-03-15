from poker_ai import PokerAI
from connection import Connection
from game_state import GameState
from time import time

conn = Connection("http://POKERWEBSITE.LOL/")
ai = PokerAI(numCores=4, timeout=3)

while True:
	# Get the state of the game
	state = conn.get()
	
	# If it's our turn, run the ai
	start = time()
	if state.my_turn():
		# Make a decision and post it
		decision = ai.make_decision(state)
		posted = conn.post(decision)
		
		# If our response didn't go through, keep trying to post for the next 3 seconds
		while not posted and time() - start < 3:
			print 'Unable to post.  Trying again...'
			posted = conn.post(decision)
		
		# Tell the user if the response was ever posted
		if posted:
			print 'Response posted.'
		else:
			print 'Error.  Unable to post response.'
