import urllib2,json
from flask import Flask, render_template
from websocket import create_connection

app = Flask(__name__)
token="xoxb-14528179959-cryA9x2tFb1SbDYppa0Xif4M"

def connect():
    url="https://slack.com/api/rtm.start?token=%s"
    url=url%(token)
    request = urllib2.urlopen(url)
    result = request.read()
    r = json.loads(result)
    return r["url"]

def recieve():
    ws = create_connection(connect())
    while True:
        result = ws.recv()
        r = json.loads(result)
        if r["type"] == "message" and "user" in r:
            message(r["channel"], "hi")
        print r

def message(channel, text):
    url="https://slack.com/api/chat.postMessage?token=%s&channel=%s&text=%s"
    url=url%(token, channel, text)
    request = urllib2.urlopen(url)

if __name__ == "__main__":
    recieve()
