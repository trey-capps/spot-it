from etl_models.extract_load_mongo import ExtractLoadMongo
from etl_models.extract_reddit_features import RedditFeatures
from etl_models.extract_reddit_songs_specific import ExtractAlternativeRock, ExtractIndieHeads
import config

MONGO_STR = config.mongocred
MONGO_DB_IN = "TempPosts"
MONGO_COL_IN = "CollectRaw"
MONGO_DB_OUT = "TempPosts"
MONGO_COL_OUT = "PostStaging"

def extract_data_from_mongo(subreddit_name):
        mongo_in = ExtractLoadMongo(MONGO_STR, MONGO_DB_IN, MONGO_COL_IN)
        mongo_in.mongo_client()
        subreddit_posts = mongo_in.filter_subreddit_posts(subreddit_name)
        print("Extracted data from raw collection")
        return subreddit_posts

def select_important_features(subreddit_posts):
    subreddit_imp_features = []
    for post in subreddit_posts:
        reddit = RedditFeatures(post["data"])
        subreddit_imp_features.append(reddit.extract_all_features())
    print("Subsetted features of interest")
    return subreddit_imp_features

def keep_only_songs(subreddit_imp_features, sub_class):
    subreddit_clean = []
    for post in subreddit_imp_features:
        filter_post = sub_class(post)

        if filter_post.is_track():
            post["track"] = filter_post.extract_track()
            post["artist"] = filter_post.extract_artist()
            subreddit_clean.append(post)
    
    print("Filtered out non-song posts")
    return subreddit_clean

def upload_to_staging(subreddit_clean):
    mongo_out = ExtractLoadMongo(MONGO_STR, MONGO_DB_OUT, MONGO_COL_OUT)
    mongo_out.mongo_connect()
    mongo_out.upload_data(subreddit_clean)
    print(f"Uploaded {len(subreddit_clean)} post(s) to {MONGO_DB_OUT}:{MONGO_COL_OUT}")

def main():
    subreddit_classes = {
        "indieheads": ExtractIndieHeads, 
        "AlternativeRock": ExtractAlternativeRock
        }

    for sub_name in subreddit_classes:
        print(f"Begin ETL pipeline for {sub_name}")
        raw_posts = extract_data_from_mongo(sub_name)
        imp_fea_posts = select_important_features(raw_posts)
        sub_class = subreddit_classes[sub_name]
        clean_posts = keep_only_songs(imp_fea_posts, sub_class)
        upload_to_staging(clean_posts)
        print(f"End ETL pipeline for {sub_name}")

if __name__ == "__main__":
    main()