import json
from os import path
from etl_operators.extract_reddit_raw import ExtractReddit
import config
import argparse
from datetime import date

#TODO: add python reddit_to_temp.py --subreddit="{subreddit}" in as BashOperator in our DAG

class IngestSubreddit:
    
    def __init__(self, subreddit, reddit_creds):
        self.subreddit = subreddit
        self.REDDIT_CREDS = reddit_creds
        self.FILE_PATH = f"./temp_data/{date.today()}_raw.json"
        #self.FILE_PATH = f"./temp_data/{date.today()}_{subreddit}_raw.json"

    def extract_data(self):
        extract_reddit = ExtractReddit(self.REDDIT_CREDS)
        extracted_posts = extract_reddit.get_subreddit_data(self.subreddit)
        reformat_post_json = {"data": extracted_posts.json()["data"]["children"]}
        return reformat_post_json
    
    def does_scrape_file_exist(self, file_path):
        if path.exists(file_path) is True:
            return True
        else:
            print("No scrape found for today...creating new one")
            return None

    def dump_json(self, data, out_file):
        with open(out_file, mode='w') as f:
            json.dump(data, f)

    def append_json(self, data, file_path):
        #Read
        with open(file_path) as f:
            existing = json.load(f)
        #Update
        existing["data"] += data["data"]
        #Load
        self.dump_json(existing, file_path)


def main(params):
    #User Input
    subreddit = params.subreddit

    #Could make user input this but will hard code for now
    REDDIT_CREDS = {
        "redditClientID": config.reddit_client_id,
        "redditSecretKey": config.reddit_secret_key,
        "redditUsername": config.reddit_username,
        "redditPass": config.reddit_pass,
        "redditUserAgent": config.reddit_user_agent
        }

    #Create class instance
    ingest_subreddit = IngestSubreddit(subreddit, REDDIT_CREDS)
    extracted_data = ingest_subreddit.extract_data() 

    if extracted_data:
        file_path = ingest_subreddit.FILE_PATH
        if ingest_subreddit.does_scrape_file_exist(file_path):
            ingest_subreddit.append_json(extracted_data, file_path)
            print(f"Appended new posts to {file_path}")
        else:
            ingest_subreddit.dump_json(extracted_data, file_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Extract raw data from subreddits")
    parser.add_argument('--subreddit', required=True, help="Subreddit Name")
    params = parser.parse_args()
    main(params)