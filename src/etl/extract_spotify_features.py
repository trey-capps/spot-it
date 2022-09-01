from etl_operators.extract_spotify_features import ExtractSpotify
from transform_reddit_posts import TransformSubreddit
import config 
from datetime import date

#Create two class instances to load json data and extract spotify features
transform_reddit = TransformSubreddit()
extract_spotify = ExtractSpotify(config.spotify_client_id, config.spotify_secret_key)

#Change in and out files for transform class
#TODO: rework classes to have path inputs and outputs as instance variables
out_file = f"./temp_data/{date.today()}_clean_features.json"
transform_reddit.FILE_OUT = out_file
in_file = f"./temp_data/{date.today()}_all_clean.json"
transform_reddit.FILE_PATH = in_file

def spotify_connect():
    print("Connected to Spotify API")
    return extract_spotify.generate_access_token()

def load_data():
    print(f"Loaded {in_file} data")
    return transform_reddit.load_json()["data"]

def append_track_features(track_data):
    new_data_with_features = []
    for post in track_data:
        artist = post["artist"]
        track = post["track"]
        track_uri = {"spotify_track_uri": extract_spotify.extract_track_uri(track, artist)}
        audio_features = extract_spotify.extract_audio_features(track_uri["spotify_track_uri"])
        spotify_data = {**post, **track_uri, **audio_features}
        new_data_with_features.append(spotify_data)
    print(f"Added audio features for {len(new_data_with_features)} tracks")
    return new_data_with_features

def export_data(data_with_features):
    transform_reddit.dump_json({"data": data_with_features}, out_file)
    print(f"Exported data to {out_file}")

def main():
    #Connect to Spotify API
    spotify_connect()
    #Load in data from temp. storage
    track_data = load_data()
    #Append track data 
    track_data_with_features = append_track_features(track_data)
    #Export tracks and their features
    export_data(track_data_with_features)

if __name__ == "__main__":
    main()