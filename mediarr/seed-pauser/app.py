from flask import Flask, request, jsonify
import requests, os

app = Flask(__name__)
app.logger.setLevel("INFO")

DELUGE_URL = f"{os.getenv("DELUGE_URL")}/json"
DELUGE_PASSWORD = os.getenv("DELUGE_PASSWORD")

RADARR_URL = os.getenv("RADARR_URL")
RADARR_API_KEY = os.getenv("RADARR_API_KEY")

JELLYFIN_URL = os.getenv("JELLYFIN_URL")
JELLYFIN_API_KEY = os.getenv("JELLYFIN_API_KEY")

session = requests.Session()

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        if not deluge_login():
            raise RuntimeError("Failed to log in to Deluge")
        playbackType = request.json['NotificationType']
        itemType = request.json['ItemType']
        torrents = get_torrents()
        torrent_ids = []

        if itemType == "Movie":
            tmdb = request.json['Provider_tmdb']
            movie = requests.get(f"{RADARR_URL}/api/v3/movie", params={"tmdbId": tmdb}, headers={"X-Api-Key": RADARR_API_KEY, "accept": "application/json"})
            file = movie.json()[0]['movieFile']['sceneName']
            torrent_ids = [tid for tid, info in torrents.items()
                           if info.get("name","") == file]
        elif itemType == "Episode":
            seriesId = request.json['SeriesId']
            series = requests.get(f"{JELLYFIN_URL}/Shows/{seriesId}/Episodes", headers={"Authorization": f"MediaBrowser Token={JELLYFIN_API_KEY}"})
            episodes = series.json()
            seriesName = episodes['Items'][0]['SeriesName']
            seasonNumber = request.json['SeasonNumber']
            episodeNumber = request.json['EpisodeNumber']

            torrent_ids = [tid for tid, info in torrents.items()
                           if seriesName in info.get("name", "") and f"S{seasonNumber:02d}" in info.get("name", "") and f"E{episodeNumber:02d}" in info.get("name", "")]
            if not torrent_ids:
                torrent_ids = [tid for tid, info in torrents.items()
                               if seriesName in info.get("name", "") and f"S{seasonNumber:02d}" in info.get("name", "")]
            if not torrent_ids:
                torrent_ids = [tid for tid, info in torrents.items()
                               if seriesName in info.get("name", "")]

        if playbackType == "PlaybackStart":
            pause_torrents(torrent_ids)
        elif playbackType == "PlaybackStop":
            resume_torrents(torrent_ids)
        
        app.logger.info(f"{playbackType}: {torrent_ids}")
        return jsonify({playbackType: len(torrent_ids), "ids": torrent_ids})
    except Exception as e:
        app.logger.error(f"{type(e)}: {str(e)}")
        return jsonify({type(e): str(e)}), 500

def deluge_rpc_call(method, params=None):
    if params is None:
        params = []
    payload = {"id": 1, "method": method, "params": params}
    r = session.post(DELUGE_URL, json=payload, timeout=10)
    r.raise_for_status()
    return r.json()

def deluge_login():
    resp = deluge_rpc_call("auth.login", [DELUGE_PASSWORD])
    return resp.get("result", False)

def get_torrents():
    fields = ["id", "name"]
    resp = deluge_rpc_call("core.get_torrents_status", [{}, fields])
    return resp.get("result", {})

def pause_torrents(torrent_ids):
    if not torrent_ids:
        return
    deluge_rpc_call("core.pause_torrent", [torrent_ids])

def resume_torrents(torrent_ids):
    if not torrent_ids:
        return 
    deluge_rpc_call("core.resume_torrent", [torrent_ids])

app.run(host="0.0.0.0", port=80)