#Create OOP Model for this file
# 
# 
# Import packages
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pymongo
import config

#Load in API information
client_credentials_manager = SpotifyClientCredentials(
    client_id=config.spotify_client_id, 
    client_secret=config.spotify_secret_key)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

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


            #Spotify Data Extraction
            #Load in API information
            client_credentials_manager = SpotifyClientCredentials(
                client_id=config.spotify_client_id, 
                client_secret=config.spotify_secret_key)
            sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
            
            #Extract song information from Spotify
            song_res = sp.search('{0} {1}'.format(artist_all, track))
            if song_res['tracks']['items'] == []:
                continue
            else:
                song_data = extract_song_data(song_res['tracks']['items'][0]['uri'])
            
            final_data = {**temp_dict, **song_data}
            
            #Add all combined data to list
            reddit_data.append(final_data)
        
        else:
            continue
        
    return reddit_data