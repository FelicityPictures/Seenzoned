import urllib2, json, sys

url = 'https://slack.com/api/channels.history'
client_id = open('token.txt','r').read()

msg = 'history.txt'

try:
    messages = open(msg,'w')
    print('creating')
    messages.close()
    print('done')
except:
    print('Something went wrong! :(')
    sys.exit(0)
