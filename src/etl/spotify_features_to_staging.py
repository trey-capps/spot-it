from etl_models.extract_load_mongo import ExtractLoadMongo
import config 

MONGO_STR = config.mongo_cred
MONGO_DB = "TempPosts"
MONGO_COL_IN = "PostStaging"
MONGO_COL_OUT = "SongStaging"

def extract_track_artist_mongo():
        mongo_in = ExtractLoadMongo(MONGO_STR, MONGO_DB, MONGO_COL_IN)
        mongo_in.mongo_connect()
        track_artist = mongo_in.select_track_artist()
        print("Extracted data from raw collection")
        return track_artist

if __name__ == "__main__":
    test = extract_track_artist_mongo()
    print(test[0])