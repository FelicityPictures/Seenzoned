import requests
import json
from websocket import create_connection

CHANNEL_NAME = raw_input('Enter channel name: ')

FILENAME = CHANNEL_NAME + '_history.txt'
BASE_URL = "https://slack.com/api/"
TOKEN = open('token.txt','r').read()[:-1]

WS = None
CHANNEL_ID = -1

def connect():
	'''
	See app.py because I just copied this from there
	'''
	global WS
	results = requests.get(BASE_URL + "rtm.start",
							params={'token': TOKEN})
	r = results.json()
	WS = create_connection(r['url'])

def get_channel_id():
	global CHANNEL_ID
	results = requests.get(BASE_URL + "channels.list",
							params={'token': TOKEN})
	r = results.json()
	for channel in r['channels']:
		if channel['name'] == CHANNEL_NAME:
			CHANNEL_ID = channel['id']

def grab_history():
	'''
	Grabs history from a certain Slack channel
	and stores it in filename.
	See app.py for comments (duplicate code)
	'''
	print 'Creating ' + FILENAME
	messages = open(FILENAME, 'w')
	
	results = requests.get(BASE_URL + "channels.history",
							params={'token': TOKEN,
									'channel': CHANNEL_ID,
									'inclusive': 1,
									'count': 1000})
	r = results.json()
	for item in r['messages']:
		if item['type'] == 'message':
			messages.write(item['text'].encode('utf8') + '\n')
	
	messages.close()
	print 'Done.'

def main():
	connect()
	get_channel_id()
	grab_history()

main()
