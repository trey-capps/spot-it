import requests
import base64
import datetime

class ExtractSpotify:
    def __init__(self, client_id, secret):
        self.client_id = client_id 
        self.secret = secret
    
    def generate_access_token(self):
        auth_url = "http://accounts.spotify.com/api/token"
        token_req = requests.post(auth_url, 
            {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.secret
            })
        token_data = token_req.json()

        if token_req.status_code == 200:
            self.access_token = token_data["access_token"]
            self.expires_in = token_data["expires_in"]
        else:
            print(f"Error generating token, Status code: {token_req.status_code}")
        
        return token_data


    def extract_relevant_tracks(self, track, artist):
        base_url = "http://api.spotify.com/v1"
        #need to encode track and artist to ease searches
        search_url = "search?q=name%3" + track + "%2artist%3" + artist + "&type=track&limit=1"

        headers = {
            "Authorization": "Bearer " + self.generate_access_token()["access_token"]
        }
        search_request = requests.get(base_url + search_url, headers=headers)
        return search_request.json()

    
    def extract_track_uri(self):
        pass

    def extract_audio_features(self):
        audio_features_url = "https://api.spotify.com/v1/audio-features/{id}"
        pass


"""class TransformSpotify:
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
    
    return song_info"""