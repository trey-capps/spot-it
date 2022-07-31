import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import etl.config as config 

client_credentials_manager = SpotifyClientCredentials(client_id=config.spotify_client_id, client_secret=config.spotify_secret_key)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

def list_playlist(user_id):
    '''
    This function will display users public playlists, future needs will change the output
    
    user_id (str): spotify username
    
    Output:
    
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

def get_song(playlist_uri):
    '''
    This function will just print songs of specified playlist
    output needs to be restructured
    
    playlist_uri (str): playlist identification (uri as of now)
    '''
    
    song_info = []
    
    playlist_songs = sp.playlist_items(playlist_uri)
    for i in range(0, len(playlist_songs['items'])):
        each_song = {}
        #Track identifier
        each_song['track_id'] = playlist_songs['items'][i]['track']['uri']
        #Track name
        each_song['track_name'] = playlist_songs['items'][i]['track']['name']
        
        #1st artists on track's identifier
        each_song['artist_id'] = playlist_songs['items'][i]['track']['artists'][0]['uri']
        #1st artists on track's name
        each_song['artist_name'] = playlist_songs['items'][i]['track']['artists'][0]['name']

        song_info.append(each_song)
        
    return song_info

def extract_song_data(track_id):
    track_feature = sp.audio_features(track_id)
    song_info = {}
    song_info['danceability'] = track_feature[0]['danceability']
    song_info['energy'] = track_feature[0]['energy']
    song_info['key'] = track_feature[0]['key']
    song_info['loudness'] = track_feature[0]['loudness']
    song_info['mode'] = track_feature[0]['mode']
    song_info['speechiness'] = track_feature[0]['speechiness']
    song_info['acousticness'] = track_feature[0]['acousticness']
    song_info['instrumentalness'] = track_feature[0]['instrumentalness']
    song_info['liveness'] = track_feature[0]['liveness']
    song_info['valence'] = track_feature[0]['valence']
    song_info['tempo'] = track_feature[0]['tempo']
    song_info['uri'] = track_feature[0]['uri']
    song_info['duration_ms'] = track_feature[0]['duration_ms']
    
    return song_info