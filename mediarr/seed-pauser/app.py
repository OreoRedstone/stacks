# deluge_pause_service.py
from flask import Flask, request, jsonify
import requests, os

# Config - change to your values
DELUGE_URL = f"{os.getenv("DELUGE_URL")}/json"   # deluge-web address
DELUGE_PASSWORD = os.getenv("DELUGE_PASSWORD")
FLASK_PORT = 80

app = Flask(__name__)
session = requests.Session()

def rpc_call(method, params=None):
    if params is None:
        params = []
    payload = {"id": 1, "method": method, "params": params}
    r = session.post(DELUGE_URL, json=payload, timeout=10)
    r.raise_for_status()
    return r.json()

def login():
    # auth.login returns True/False
    resp = rpc_call("auth.login", [DELUGE_PASSWORD])
    return resp.get("result", False)

def get_torrents_status():
    # request a compact set of fields; add other fields you need
    # fields = ["id", "name", "state", "progress", "total_size"]
    fields = ["id", "state", "progress"]
    resp = rpc_call("core.get_torrents_status", [{}, fields])
    return resp.get("result", {})

def pause_torrents(torrent_ids):
    if not torrent_ids:
        return {"paused": 0}
    resp = rpc_call("core.pause_torrent", [torrent_ids])
    return resp

def resume_torrents(torrent_ids):
    if not torrent_ids:
        return {"resumed": 0}
    resp = rpc_call("core.resume_torrent", [torrent_ids])
    return resp

@app.route("/pause_seeding", methods=["POST"])
def pause_seeding():
    try:
        torrents = get_torrents_status()
        # Filter: state equals "Seeding" OR progress == 100
        seeding_ids = [tid for tid, info in torrents.items()
                       if info.get("state","").lower() == "seeding" or float(info.get("progress",0)) >= 100.0]
        pause_torrents(seeding_ids)
        return jsonify({"paused": len(seeding_ids), "ids": seeding_ids})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/resume_seeding", methods=["POST"])
def resume_seeding():
    try:
        torrents = get_torrents_status()
        # Filter: state equals "Seeding" OR progress == 100
        seeding_ids = [tid for tid, info in torrents.items()
                       if info.get("state","").lower() == "paused" and float(info.get("progress",0)) >= 100.0]
        resume_torrents(seeding_ids)
        return jsonify({"resumed": len(seeding_ids), "ids": seeding_ids})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    if login():
        app.run(host="0.0.0.0", port=FLASK_PORT)
    else:
        print("Failed to authenticate.")
