import urllib2,json
from flask import Flask, render_template
from websocket import create_connection

app = Flask(__name__)
token="xoxb-14526704643-twywi1tueSBhidtlaLb3sR0M"

def connect():
    url="https://slack.com/api/rtm.start?token=%s"
    url=url%(token)
    request = urllib2.urlopen(url)
    result = request.read()
    r = json.loads(result)
    return r["url"]

def userid(username):
    url="https://slack.com/api/users.list?token=%s"
    url=url%(token)
    request = urllib2.urlopen(url)
    result = request.read()
    r = json.loads(result)
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
        url="https://slack.com/api/users.list?token=%s"
        url=url%(token)
        request = urllib2.urlopen(url)
        result = request.read()
        r = json.loads(result)


def recieve():
    ws = create_connection(connect())
    while True:
        result = ws.recv()
        r = json.loads(result)
        if r["type"] == "message" and r["channel"] == "G0E1ERJUB" and "user" in r:
            message(r["channel"], "hi")
        print r

def message(channel, text):
    url="https://slack.com/api/chat.postMessage?token=%s&channel=%s&text=%s&username=MarkovBot"
    url=url%(token, channel, text)
    request = urllib2.urlopen(url)

if __name__ == "__main__":
    recieve()
