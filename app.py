"""
Roy Xu
Main file for exchange of information between bot and slack api
"""

import requests
import json
from flask import Flask, render_template
from websocket import create_connection
import markov
from sys import argv
from messages import *

app = Flask(__name__)
token = "xoxb-14526704643-twywi1tueSBhidtlaLb3sR0M" #token for markovbot in stuycs slack
DEBUG = False

def connect():
    """
    Connects to rtm.start and creates a new real time messaging session.
    Allows for the slack api to send info when certain events, such as
    a sent message, are triggered.

    Returns:
        A websocket url that is connected to in the receive() method.
    """

    results = requests.get("https://slack.com/api/rtm.start",  #connects to rtm.start with token
                           params={'token': token})  #results sent back by slack api.
    r = results.json()  #results placed in json format
    return r["url"]  #websocket url from results


def userid(username):
    """
    Finds the userid of a user by their real name. Slack lists user in its api
    results by a unique id. Users on slack see the real name of a user.
    Users.list returns a list of all users on slack with their userid as well
    as their real name. Loops through to find which user matches the userid.
    Will not work if users do not set a real name.

    Args:
        username: A slack user's real name.

    Returns:
        the userid associated with the username.
        0 if username does not exist
    """

    results = requests.get("https://slack.com/api/users.list",  #connects to users.list with token
                           params={'token': token})  #results sent back by slack api
    r = results.json()  #results placed in json form
    for member in (r["members"]):  #loops through list of members
        if "real_name" in member:  #checks if real name is defined
            if username == member["real_name"].lower():  #checks username equality
                return(member["id"])  #returns id
    return 0  #returns 0 if member does not exist

def username(userid):
    """
    Finds username from userid. Opposite of userid()

    Args:
        userid: A slack user's hidden userid

    Returns:
        username associated with the userid
    """
    results = requests.get("https://slack.com/api/users.list",  #connects to users.list with token
                           params={'token': token})  #results sent back by slack api
    r = results.json()  #results placed in json form
    for member in (r["members"]):  #loops through list of members
        if "real_name" in member:  #checks if real name is defined
            if userid == member["id"]:  #checks id equality
                return(member["real_name"])  #returns username
    return 0  #returns 0 if member does not exist



def directMessage(username):
    """
    Opens a direct message channel with another user with username. Allows the bot
    to send private messages to users.

    Args:
        username: A slack user's real name

    Returns:
        Returns the direct message channel id
    """

    # calls userid() method to return userid from username
    id = userid(username)
    if id == 0:  # userid(username) returns 0 if user doesn't exist
        return 0  # returns 0 if user doesn't exist
    else:
        return directMessageUID(id)  # passes to directMessageUID() method


def directMessageUID(userid):
    """
    Opens a direct message channel with another user with userid. Allows the bot
    to send private messages to users.

    Args:
        userid: slack user's userid

    Returns:
        Returns the direct message channel id
    """
    results = requests.get("https://slack.com/api/im.open",  # connects to im.open with token and userid
                           params={'token': token, 'user': userid})
    r = results.json()
    return r["channel"]["id"]  # returns channel id


def receive():
    """
    Opens a websocket to Slack RTM and allows for communication from the
    slack api. Allows detection of events such as messages being sent. Runs in
    a loop that constantly checks for events being sent.
    """

    ws = create_connection(connect()) #connects to websocket url returned from connect() method
    while True: #continuous loop
        results = ws.recv() #receive results from websocket
        r = json.loads(results)
        if DEBUG:
            print r #logs events in console

        if "channel" in r:
            markov_dict = get_proper_dict(r["channel"])

        if r["type"] == "message" and "user" in r: #checks if event is message and is not from a bot

            if "speak like" in r["text"].lower():
                begin_index = r["text"].find("speak like") + len("speak like ")
                desired_channel = r["text"][begin_index:]
                desired_id = get_channel_id(False, desired_channel)
                markov_dict = get_proper_dict(desired_id)
                msg = markov.get_sentence(markov_dict) #pulls sentences from markov.py
                message(r["channel"], msg)

            elif r["text"].lower() == "//markov speak to me": #checks if message is a command to markovbot
                channel = directMessageUID(r["user"]) #direct messages user"
                message(channel, "Hello")

            elif (r["text"].lower()).startswith("//markov speak to "): #checks if message is a command to markovbot
                channel = directMessage((r["text"].lower())[18:]) #direct messages the user markovbot is told to message
                if channel == 0: #checks if user exists
                    message(r["channel"], "User not Found")
                else:
                    msg = "Hello, %s sent me" % (username(r["user"])) #sends Hello and whoever sent command to target of command
                    message(channel, msg)

            else:
                msg = markov.get_sentence(markov_dict) #pulls sentences from markov.py
                message(r["channel"], msg) #otherwise send a response to channel

def get_proper_dict(channel_id):
    """
    get_proper_dict: returns a proper markov dictionary based on channel name

    Args:
        channel_id (string): id of the channel
    
    Returns:
        a markov dictionary based on the channel name or based on
        softdev_history if unsuccessful    
    """

    try:
        markov_dict = markov.get_dictionary("history/" + channel_id + '_history.txt')
        print "file found!"
    except IOError, FileNotFoundError: # if we don't have history for it
        try:
            grab_history(channel_id, False)
            markov_dict = markov.get_dictionary("history/" + channel_id + '_history.txt')
            print "file generated!"
        except:
            # default = softdev channel
            markov_dict = markov.get_dictionary("history/C0ADBSKC4_history.txt")
            print "using default"

    except:
        # default = softdev channel
        markov_dict = markov.get_dictionary("history/C0ADBSKC4_history.txt")
        print "using default"

    if markov_dict == {}: # maybe its private
        try:
            grab_history(channel_id, True)
            markov_dict = markov.get_dictionary("history/" + channel_id + '_history.txt')
            print "new file generated!"
        except:
            # default = softdev channel
            markov_dict = markov.get_dictionary("history/C0ADBSKC4_history.txt")
            print "using default"

        if markov_dict == {}: # idk what happened
            markov_dict = markov.get_dictionary("history/C0ADBSKC4_history.txt")
            print "using default because empty dictionary"
       
    return markov_dict

def message(channel, text):
    """
    Sends a message to the specified channel with a specified message

    Args:
        channel: the channel id of where to send the message
        text: the message to be sent
    """

    results = requests.get("https://slack.com/api/chat.postMessage", #connects to chat.postMessage with token, channel, text, username
                           params={'token': token, 'channel': channel, 'text': text, 'username': "MarkovBot"})

if __name__ == "__main__":
    if "-d" in argv:
        DEBUG = True
    grab_history(get_channel_id(False, "softdev"), False)
    receive() #runs main loop
