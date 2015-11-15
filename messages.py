import requests
import json
from websocket import create_connection
import re

TOKEN = open('token.txt','r').read()[:-1]
BASE_URL = "https://slack.com/api/"

def get_channel_id(is_private, channel_name):
    """
    get_channel_id: gets the channel id based on the channel name and its
    privacy seetings

    Args:
        is_private (boolean): if the channel is private
	channel_name (string): the name of the channel
    
    Returns:
        a string that is the channel_id    
    """

    HTTPS_method = "groups.list" if is_private else "channels.list";
    category = 'groups' if is_private else 'channels'
    results = requests.get(BASE_URL + HTTPS_method, params={'token': TOKEN})
    r = results.json()
    for channel in r[category]:
        if channel['name'] == channel_name:
            return channel['id']

def grab_history(channel_id, is_private):
    """
    grab_history: gets history of channel based on the id and stores it in a
    history file named as "<channel_id>_history.txt"

    Args:
	channel_id (string): id of the desired channel
        is_private (boolean): is the channel private?
    
    Returns:
        void
    
    Example:
        grab_history(get_channel_id(False, "softdev"), False) --> creates
        the file <id of softdev>_history.txt
    
    Raises:
        IOError - if the file cannot be written
    """
    messages = open("history/" + channel_id + "_history.txt", 'w')
    
    HTTPS_method = "groups.history" if is_private else "channels.history"
    results = requests.get(BASE_URL + HTTPS_method, params={'token': TOKEN,
                                                            'channel':channel_id,
                                                            'inclusive': 1,
                                                            'count': 1000})
    r = results.json()

    for item in r['messages']:
        if item['type'] == 'message':
            s = item['text'].encode('utf8') + '\n'
            # @channel, etc.
            p = re.compile('(<!)')
            s = p.sub('@', s)
            # <@USER_ID
            p = re.compile('(<@[a-zA-z0-9]{9}\|)')
            s = p.sub('@', s)
            # remaining <>
            p = re.compile('([<>])')
            s = p.sub('', s)
            messages.write(s);
    
    messages.close()

if __name__ == '__main__':
    CHANNEL_NAME = raw_input('Enter channel name: ')
    IS_PRIVATE = raw_input('Private group?[y/n] ').strip().lower()
    IS_PRIVATE = IS_PRIVATE == 'yes' or IS_PRIVATE == 'y'

    ID = get_channel_id(IS_PRIVATE, CHANNEL_NAME)
    grab_history(ID, IS_PRIVATE)
