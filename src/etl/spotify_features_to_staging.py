from etl_models.extract_load_mongo import ExtractLoadMongo
from etl_models.extract_spotify_features import ExtractSpotify
import config 

MONGO_STR = config.mongo_cred
MONGO_DB = "TempPosts"
MONGO_COL_IN = "PostStaging"
MONGO_COL_OUT = "SongStaging"

extract_spotify = ExtractSpotify(config.spotify_client_id, config.spotify_secret_key)

def extract_track_artist_mongo():
        mongo_in = ExtractLoadMongo(MONGO_STR, MONGO_DB, MONGO_COL_IN)
        mongo_in.mongo_client()
        track_artist = mongo_in.select_track_artist()
        print("Extracted data from raw collection")
        return track_artist

def spotify_connect():
        extract_spotify.generate_access_token()
        print("Successfully connected to Spotify API")
        return 

def extract_spofity_features(track_artist):
        track = track_artist["track"]
        artist = track_artist["artist"]
        track_info = {"track": track, "artist": artist}
        track_uri = extract_spotify.extract_track_uri(track, artist)
        track_info["track_uri"] = track_uri
        audio_features = extract_spotify.extract_audio_features(track_uri)
        return {**track_info, **audio_features}

def upload_track_features(track_features):
        mongo_out = ExtractLoadMongo(MONGO_STR, MONGO_DB, MONGO_COL_OUT)
        mongo_out.mongo_client()
        mongo_out.upload_data(track_features)
        print(f"Successfully uploaded {len(track_features)} track(s) with features to {MONGO_COL_OUT}")

def main():
        spotify_connect()
        track_artist_all = extract_track_artist_mongo()
        audio_features_all = []
        for track_artist in track_artist_all:
                audio_features = extract_spofity_features(track_artist)
                audio_features_all.append(audio_features)
                print(f"Added {track_artist['track']}")
        upload_track_features(audio_features_all)

if __name__ == "__main__":
    main()