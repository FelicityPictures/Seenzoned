import urllib2,json
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def message():
    client_id="14048866565.14274502486"
    url="https://slack.com/oauth/authorize?client_id=%s&scope=channels:write"
    url=url%(client_id)
    request = urllib2.urlopen(url)
    return "hi"



if __name__ == "__main__":
   app.debug = True
   app.run(host="0.0.0.0", port=8000)
