import urllib, urllib2
import json
from game_state import GameState

# This class is used for HTTP POST and GET when communicating with a server
class Connection:
	def __init__(self, url):
		self.url = url
		self.headers = {"Content-type": "application/json"}
		
	def get(self):
		try:
			response = urllib2.urlopen(self.url)
			html = response.read()
			return GameState(html)
		except:
			return None
		
		
	def post(self, params):
		try:
			req = urllib2.Request(self.url, params)
			response = urllib2.urlopen(req)
			html = response.read()
			return html is None
		except:
			return False
