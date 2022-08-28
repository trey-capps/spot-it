import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials(client_id='89f0f6cd2e6d44579b37a8742c6efe2e', client_secret='620faa6d1e704e3d89046ff2ef0b3a70')
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

def get_song(playlist_uri):
    '''
    This function will just print songs of specified playlist
    output needs to be restructured
    
    playlist_uri (str): playlist identification (uri as of now)
    
    Output:
    
    song_info: json format with each songs name and artist (uri included)
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