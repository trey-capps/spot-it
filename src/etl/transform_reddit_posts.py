from ingest_reddit_raw import IngestSubreddit
from etl_operators.extract_reddit_features import RedditFeatures
from etl_operators.extract_reddit_songs_specific import *

import json
from datetime import date

class TransformSubreddit(IngestSubreddit):

    #Add mapping of subreddits and their track transformations
    #Update this map as more subreddits are added
    SUBREDDIT_MAP = {
        "indieheads": ExtractIndieHeads,
        "Alternativerock": ExtractAlternativeRock
        }

    def __init__(self):
        self.FILE_PATH = f"./temp_data/{date.today()}_raw.json"
        #self.FILE_PATH = f"./temp_data/{date.today()}_{subreddit}_raw.json"
        self.FILE_OUT = f"./temp_data/{date.today()}_all_clean.json"

    def load_json(self): 
        with open(self.FILE_PATH) as f:
            raw_data = json.load(f)
        return raw_data

    def select_important_features(self, subreddit_data):
        extracted_features = []
        for post in subreddit_data:
            #Filter using method from custom classes
            reddit = RedditFeatures(post["data"])
            extracted_features.append(reddit.extract_all_features())

        print(f"Subsetted features of interest")
        return extracted_features

    def filter_tracks(self, subreddit_data_clean):
        subreddit_clean = []
        for post in subreddit_data_clean:
            subreddit = post["subreddit"]
            #Select class for extraction and create instance
            subreddit_track_extractor = self.SUBREDDIT_MAP[subreddit](post)

            if subreddit_track_extractor.is_track():
                post["track"] = subreddit_track_extractor.extract_track()
                post["artist"] = subreddit_track_extractor.extract_artist()
                subreddit_clean.append(post)

        print(f"Filtered out non-song posts")
        return subreddit_clean

def main():
    #Create class instance
    transform_subreddit = TransformSubreddit()
    out_path = transform_subreddit.FILE_OUT

    try:
        raw_data = transform_subreddit.load_json()["data"]
        subset_data = transform_subreddit.select_important_features(raw_data)
        track_data = transform_subreddit.filter_tracks(subset_data)
        #Check if file already exists
        if transform_subreddit.does_scrape_file_exist(out_path):
            #Append
            transform_subreddit.append_json({"data": track_data}, out_path)
            print(f"Appended new posts to {out_path}")
        else:
            #Create new file
            transform_subreddit.dump_json({"data": track_data}, out_path)
        
    except FileNotFoundError:
        print(f"Data has not been scraped today")

if __name__ == '__main__':
    main()