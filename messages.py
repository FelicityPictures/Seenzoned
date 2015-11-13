import urllib2, json, sys

url = 'https://slack.com/api/channels.history'
client_id = open('token.txt','r').read()
filename = 'history.txt'
channel = ''

grab_history():
	'''
	Grabs history from a certain Slack channel
	and stores it in filename
	'''
	#try:
	#    messages = open(msg,'w')
	#    print('creating')
	#    messages.close()
	#    print('done')
	#except:
	#    print('Something went wrong! :(')
	#    sys.exit(0)
	messages = open(filename, 'w')
	print 'creating ' + filename
	messages.close()
	print 'done'
