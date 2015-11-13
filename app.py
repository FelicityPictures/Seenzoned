import requests, json
from flask import Flask, render_template
from websocket import create_connection
import markov

app = Flask(__name__)
token="xoxb-14526704643-twywi1tueSBhidtlaLb3sR0M"

def connect():
    results = requests.get("https://slack.com/api/rtm.start",
              params={'token': token})
    r = results.json()
    return r["url"]

def userid(username):
    results = requests.get("https://slack.com/api/users.list",
              params={'token': token})
    r = results.json()
    for member in (r["members"]):
        if "real_name" in member:
            if username == member["real_name"]:
                return(member["id"])
    return 0

def directMessage(username):
    userid = userid(username)
    if userid == 0:
        print("Not Found")
    else:
        results = requests.get("https://slack.com/api/im.open",
                  params={'token': token, 'user': userid})
        r = results.json()
        return r["channel"]["id"]

def directMessageUID(userid):
    results = requests.get("https://slack.com/api/im.open",
              params={'token': token, 'user': userid})
    r = results.json()
    return r["channel"]["id"]


def receive():
    ws = create_connection(connect())
    while True:
        results = ws.recv()
        r = json.loads(results)
        print r
        msg = markov.get_sentence(markov.init())
        if r["type"] == "message" and "user" in r:
            if r["text"].lower() == "speak to me":
                channel = directMessageUID(r["user"])
                message(channel, "Hello")
            else:
                message(r["channel"], str(msg))

def message(channel, text):
    results = requests.get("https://slack.com/api/chat.postMessage",
              params={'token': token, 'channel': channel, 'text': text, 'username': "MarkovBot"})

if __name__ == "__main__":
    receive()
