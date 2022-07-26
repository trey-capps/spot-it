from flask import Flask, request
import json
from pymongo import MongoClient
import spot_collect as sc

app = Flask(__name__)

CONN_STRING = ""
with open("credentials.json", "r") as cred:
    CONN_STRING = json.load(cred)["connectionStr"]
client = MongoClient(CONN_STRING)

@app.route("/getCollections")
def get_collections():
    db = client['RedditCollect']
    items = db.list_collection_names()
    return {"data": items}

@app.route("/<string:subreddit>/data/<int:rows>")
def get_sub_data(subreddit, rows):
    #add error handling for subreddits not in collection
    
    db = client['RedditCollect']
    collection = db[subreddit]
    
    #query recent 'rows' amount of reddit posts
    songs = list(collection.find({}).limit(rows))

    return {"data": songs}

@app.route("/userPlaylist", methods=["GET","POST"])
def get_user_playlist():
    if request.method == 'POST':
        spotify_username = request.form['spotifyUsername']
    
    playlists = sc.list_playlist(spotify_username)

    return {"data": playlists}

@app.route("/userPlaylist", methods=["GET","POST"])
def get_user_playlist():
    if request.method == 'POST':
        spotify_username = request.form['playlistUri']
    
    playlists = sc.list_playlist(spotify_username)

    return {"data": playlists}

#recommend songs (post/put, get)


if __name__ == "__main__":
    app.run(debug=True)