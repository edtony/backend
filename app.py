#! /usr/bin/env python
import os
import requests
from flask import Flask
from flask_cors import CORS
from base64 import b64encode
from urllib.parse import urlencode


app = Flask(__name__)
CORS(app)


@app.route("/ping")
def ping():
    return "pong"


@app.route("/docs/<pdf>")
def doc(pdf):
    with open(f"./docs/{pdf}", "rb") as f:
        data = f.read()
        data = b64encode(data).decode("utf-8")
    return f"data:application/pdf;base64,{data}"


@app.route("/youtube/<channel>")
def youtube(channel):
    params = {
        "channelId": channel,
        "maxResults": 25,
        "order": "date",
        "part": "snippet",
        "key": os.environ["API_KEY"],
    }
    response = requests.get("https://youtube.googleapis.com/youtube/v3/search?" + urlencode(params))
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    port = os.getenv("PORT", 5000)
    app.run(host="0.0.0.0", port=port)
