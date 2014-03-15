from test_ai import PokerAI
from connection import Connection
from game_state import GameState
from time import time

conn = Connection("http://nolimitcodeem.com/api/players/239f6725-021f-4637-abc8-d78ade95649a/")

ai = PokerAI(numCores=4, timeout=3)
json = '{\
    "name": "Bill13",\
    "your_turn": true,\
    "initial_stack": 250,\
    "stack": 215,\
    "current_bet": 35,\
    "call_amount": 0,\
    "hand": ["AH", "JD"],\
    "community_cards":  ["QD", "7D", "KH", "AD"],\
    "betting_phase": "draw",\
    "players_at_table": [{\
        "player_name": "Bill12",\
        "initial_stack": 250,\
        "current_bet": 35,\
        "stack": 215,\
        "folded": false,\
        "actions": [{\
            "action": "ante",\
            "amount": 10\
        }, {\
            "action": "bet",\
            "amount": 25\
        }, {\
            "action": "replace",\
            "cards": ["6S", "AD"]\
        }]\
    }, {\
        "player_name": "Bill13",\
        "initial_stack": 250,\
        "current_bet": 35,\
        "stack": 215,\
        "folded": false,\
        "actions": [{\
            "action": "ante",\
            "amount": 10\
        }, {\
            "action": "bet",\
            "amount": 0\
        }]\
    }],\
    "total_players_remaining": 2,\
    "table_id": 766,\
    "round_id": 823,\
    "round_history": [{\
        "round_id": 823,\
        "table_id": 766,\
        "stack_change": null\
    }],\
    "lost_at": null\
}'

def variance(vals):
	avg = sum(vals) / len(vals)
	var = 0
	for val in vals:
		var += (avg - val) ** 2
	return var

state = GameState(json)

wins = []
for i in range(25):
	prob = ai.make_decision(state)
	wins.append(prob)

var = variance(wins)
print 'Average win_prob:', sum(wins) / len(wins)
print 'Variance of wins:', var
print 'Standard deviation:', var ** 0.5
print 'Low value:', min(wins), '\tHigh value:', max(wins)
