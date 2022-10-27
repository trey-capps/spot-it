#USER LOGIN
#USER SELECT PLAYLIST
#click spot it
#CREATE MODEL USING SCRIPT
#LOAD MODEL
#click find new songs
#ASSIGN REDDIT SONGS TO CLUSTERS

from flask import Flask, render_template, request
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import credentials

client_credentials_manager = SpotifyClientCredentials(client_id=credentials.spotify_client_id, client_secret=credentials.spotify_secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

def list_playlist(user_id):
    '''
    This function will display users public playlists, future needs will change the output
    user_id (str): spotify username
    Output:
    playlists (list): list of all the public playlists of the user
    '''
    play_name = []
    play_uri = []
    
    playlist = sp.user_playlists(user_id)
    for i in range(0, len(playlist['items'])):
        play_name.append(playlist['items'][i]['name'])
        play_uri.append(playlist['items'][i]['uri'])
    
    #Use playlist name as key and uri as value
    playlists = dict(zip(play_name, play_uri))
    
    return playlists

app = Flask(__name__)

@app.route("/home")
def root():
    return render_template("form.html")

@app.route("/userPlaylists",methods = ["POST", "GET"])
def result():

    if request.method == "POST":
        result = request.form
        playlists = list_playlist(result['spotifyUserName'])
        json_result = dict(result)
        print(json_result)
        return render_template("results.html", result=result, playlists=playlists)

if __name__ == "__main__":
    app.run(debug = True)