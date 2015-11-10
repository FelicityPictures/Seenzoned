import urllib2, json

url = 'https://slack.com/api/channels.history'

file = open('token.txt','r').read()
client_id = ''
