import requests

class ExtractSpotify:
    def __init__(self, track, artist):
        self.track = track 
        self.artist = artist 

    def connect_spotify(self):
        pass

    def extract_feautres(self):
        # post artist, track

        # return json
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