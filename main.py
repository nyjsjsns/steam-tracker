import requests
import time
import threading
from flask import Flask, jsonify, render_template
from datetime import datetime
import json
import os

app = Flask(__name__)

STEAM_API_KEY = os.getenv("63336F1C1D1F2C54C4C4E06B3E5D766B")
STEAM_ID = os.getenv("76561199018299083")

status_history = []

def get_player_status():
    url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={STEAM_ID}"
    try:
        response = requests.get(url)
        data = response.json()
        personastate = data["response"]["players"][0]["personastate"]
        return personastate
    except Exception as e:
        print("Error getting Steam data:", e)
        return None

def track_status():
    while True:
        status = get_player_status()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if status is not None:
            status_history.append((timestamp, status))
        time.sleep(60)

@app.route("/")
def index():
    return render_template("index.html", status_history=status_history)

if __name__ == "__main__":
    threading.Thread(target=track_status, daemon=True).start()
    app.run(host="0.0.0.0", port=8080)
