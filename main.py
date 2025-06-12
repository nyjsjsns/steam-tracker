import requests import time import threading from flask import Flask, jsonify, render_template from datetime import datetime import json import os

app = Flask(name)

API_KEY = '63336F1C1D1F2C54C4C4E06B3E5D766B' STEAM_ID64 = '76561199018399083'

LOG_FILE = 'log.json' CHECK_INTERVAL = 60  # Sekunden

status_log = []

Lade alten Log (wenn vorhanden)

if os.path.exists(LOG_FILE): with open(LOG_FILE, 'r') as f: try: status_log = json.load(f) except: status_log = []

def steam_status(): url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={API_KEY}&steamids={STEAM_ID64}" try: r = requests.get(url) data = r.json() player = data['response']['players'][0] state = player.get('personastate', 0) status_map = { 0: "Offline", 1: "Online", 2: "Busy", 3: "Away", 4: "Snooze", 5: "Looking to trade", 6: "Looking to play" } return status_map.get(state, "Unknown") except Exception as e: return "Error"

def log_status_periodically(): while True: status = steam_status() now = datetime.now().strftime("%Y-%m-%d %H:%M:%S") status_log.append({"time": now, "status": status}) with open(LOG_FILE, 'w') as f: json.dump(status_log, f) time.sleep(CHECK_INTERVAL)

@app.route('/') def index(): return render_template('index.html')

@app.route('/api/statuslog') def get_status_log(): return jsonify(status_log[-1440:])  # max 1 Tag zurück

if name == "main": thread = threading.Thread(target=log_status_periodically, daemon=True) thread.start() app.run(host='0.0.0.0', port=8080)

