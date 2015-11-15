import requests
import json
from websocket import create_connection
import re

CHANNEL_NAME = raw_input('Enter channel name: ')
IS_PRIVATE = raw_input('Private group?[y/n] ').strip().lower()
IS_PRIVATE = IS_PRIVATE == 'yes' or IS_PRIVATE == 'y'

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
	HTTPS_method = "groups.list" if IS_PRIVATE else "channels.list";
	category = 'groups' if IS_PRIVATE else 'channels'
	results = requests.get(BASE_URL + HTTPS_method,
							params={'token': TOKEN})
	r = results.json()
	for channel in r[category]:
		if channel['name'] == CHANNEL_NAME:
			CHANNEL_ID = channel['id']

def grab_history():
	'''
	Grabs history from a certain Slack channel
	and stores it in filename.
	See app.py for comments (duplicate code)
	'''
	print 'Writing ' + FILENAME
	messages = open(FILENAME, 'w')
	
	HTTPS_method = "groups.history" if IS_PRIVATE else "channels.history"
	print HTTPS_method
	results = requests.get(BASE_URL + HTTPS_method,
							params={'token': TOKEN,
									'channel': CHANNEL_ID,
									'inclusive': 1,
									'count': 1000})
	r = results.json()
	print r
	for item in r['messages']:
		if item['type'] == 'message':
			s = item['text'].encode('utf8') + '\n'
			# @channel, etc.
			p = re.compile('(<!)')
			s = p.sub('@', s)
			# <@USER_ID
			p = re.compile('(<@[a-zA-z0-9]{9}\|*)')
			s = p.sub('', s)
			# remaining <>
			p = re.compile('([<>])')
			s = p.sub('', s)
			messages.write(s);
	
	messages.close()
	print 'Done.'

def main():
	connect()
	get_channel_id()
	grab_history()

main()
