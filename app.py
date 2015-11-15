"""
Roy Xu
Main file for exchange of information between bot and slack api
Currently restricted to Markov-Bot-Testing Channel (Line 131)
"""

import requests
import json
from flask import Flask, render_template
from websocket import create_connection
import markov

app = Flask(__name__)
f = open("token.txt", "r")
TOKEN = f.readline()[:-1] #TOKEN for markovbot in stuycs slack
f.close()

def connect():
    """
    Connects to rtm.start and creates a new real time messaging session.
    Allows for the slack api to send info when certain events, such as
    a sent message, are triggered.

    Returns:
        A websocket url that is connected to in the receive() method.
    """

    results = requests.get("https://slack.com/api/rtm.start",  #connects to rtm.start with TOKEN
                           params={'token': TOKEN})  #results sent back by slack api.
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

    results = requests.get("https://slack.com/api/users.list",  #connects to users.list with TOKEN
                           params={'token': TOKEN})  #results sent back by slack api
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
    results = requests.get("https://slack.com/api/users.list",  #connects to users.list with TOKEN
                           params={'token': TOKEN})  #results sent back by slack api
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
    results = requests.get("https://slack.com/api/im.open",  # connects to im.open with TOKEN and userid
                           params={'token': TOKEN, 'user': userid})
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
        print r #logs events in console
        msg = markov.get_sentence(markov.init()) #pulls sentences from markov.py
        if r["type"] == "message" and "user" in r and r["channel"] == "G0EHEV69G": #checks if event is message and is not from a bot plus restriction to only one channel
            if r["text"].lower() == "//markov speak to me": #checks if message is a command to markovbot
                channel = directMessageUID(r["user"]) #direct messages user"
                message(channel, "Hello")
            elif (r["text"].lower())[:18] == "//markov speak to ": #checks if message is a command to markovbot
                channel = directMessage((r["text"].lower())[18:]) #direct messages the user markovbot is told to message
                if channel == 0: #checks if user exists
                    message(r["channel"], "User not Found")
                else:
                    msg = "Hello, %s sent me" % (username(r["user"])) #sends Hello and whoever sent command to target of command
                    message(channel, msg)
            else:
                message(r["channel"], str(msg)) #otherwise send a response to channel


def message(channel, text):
    """
    Sends a message to the specified channel with a specified message

    Args:
        channel: the channel id of where to send the message
        text: the message to be sent
    """

    results = requests.get("https://slack.com/api/chat.postMessage", #connects to chat.postMessage with TOKEN, channel, text, username
                           params={'token': TOKEN, 'channel': channel, 'text': text, 'username': "MarkovBot"})

if __name__ == "__main__":
    receive() #runs main loop
