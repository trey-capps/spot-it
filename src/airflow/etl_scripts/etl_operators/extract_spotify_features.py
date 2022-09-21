from typing import Dict
from urllib.parse import urlencode
import requests
import base64

class ExtractSpotify:
    def __init__(self, client_id: str, secret: str) -> None:
        self.client_id = client_id 
        self.secret = secret
    
    def create_access_token_data(self) -> Dict:
        """Specify grant type"""
        return {"grant_type": "client_credentials"}
    
    def create_access_token_headers(self) -> Dict:
        """Create request headers for Spotify API"""
        credentials = f"{self.client_id}:{self.secret}"
        credentials_bytes = credentials.encode('ascii')
        credentials_b64_bytes = base64.b64encode(credentials_bytes)
        credentials_b64_header = credentials_b64_bytes.decode('ascii')
        return {"Authorization": f"Basic {credentials_b64_header}"}
    
    def generate_access_token(self) -> Dict:
        """Generate Spotify API access token"""
        auth_url = "https://accounts.spotify.com/api/token"
        token_data = self.create_access_token_data()
        token_headers = self.create_access_token_headers()
        token_req = requests.post(auth_url, headers=token_headers, data=token_data) 
            
        token_data = token_req.json()
        if token_req.status_code == 200:
            self.access_token = token_data["access_token"]
            self.expires_in = token_data["expires_in"]
            self.spotify_header = {"Authorization": f"Bearer {self.access_token}"}
        else:
            print(f"Error generating token, Status code: {token_req.status_code}")
        
        return token_data

    def extract_relevant_tracks(self, track: str, artist: str) -> Dict:
        """
        Return the first displayed track from Spotify API request
        track (str): track name
        artist (str): artist name
        """
        base_url = "https://api.spotify.com/v1/search"
        search_data = urlencode({
            "q": f"{track} {artist}",
            "type": "track",
            "limit": "1"})
        search_url = f"{base_url}?{search_data}"
        
        search_request = requests.get(search_url, headers=self.spotify_header)
        return search_request.json()

    def extract_track_uri(self, track: str, artist: str) -> str:
        """
        Extract the track uri from the Spotify API request
        track (str): track name
        artist (str): artist name
        """
        search_json = self.extract_relevant_tracks(track, artist)
        try:
            track_uri = search_json['tracks']['items'][0]['id']
            return track_uri
        except IndexError:
            return None
        
    def extract_audio_features(self, track_uri: str) -> str:
        """
        Extract audio feature data points for specified track_uri
        track_uri (str): track uri (provided from Spotify)
        """
        audio_features_url = f"https://api.spotify.com/v1/audio-features/{track_uri}"
        audio_feature_request = requests.get(audio_features_url, headers=self.spotify_header)
        return audio_feature_request.json()