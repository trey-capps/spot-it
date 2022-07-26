import requests
import json
import pymongo
import argparse

#Load in API keys
with open("./credentials.json", "r") as cred:
    credentials = json.load(cred)

    CLIENT_ID = credentials["redditClientID"]
    SECRET_KEY = credentials["redditSecretKey"]
    USERNAME = credentials["redditUsername"]
    PASS = credentials["redditPass"]
    USER_AGENT = credentials["redditUserAgent"]
    MONGO_CRED = credentials["mongoString"]

# Documentation : https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example
client_auth = requests.auth.HTTPBasicAuth(f"{CLIENT_ID}", f"{SECRET_KEY}")
post_data = {"grant_type": "password", "username": f"{USERNAME}", "password": f"{PASS}"}
headers = {"User-Agent": f"{USER_AGENT}"}

### Reddit - Extract
def get_access_token():
    """Get access token from Reddit API"""
    try:
        response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
        #Save Token 
        token_type = response.json()['token_type']
        access_token = response.json()['access_token']
        return {"Authorization": f"{token_type} {access_token}", **headers} #Now send GET requests to "https://oauth.reddit.com"
    except:
        print(f"Error generating token, status code: {response.status_code}")

def get_subreddit_data(subreddit, headers):
    """Generate post request with access tokens to gather post data"""
    #Add testing as to whether that is an actual subreddit
    try:
        get_posts = requests.get(f"https://oauth.reddit.com/r/{subreddit}/new", headers=headers)
        if get_posts.status_code == 200:
            print(f"Collected 25 posts from r/{subreddit}")
            return get_posts
        else:
            raise
    except:
        print(f"Error getting posts, status code: {get_posts.status_code}")

### MongoDB - Load
def mongo_connection():
    """PyMongo client""" 
    return pymongo.MongoClient(MONGO_CRED)

def select_collection(client, database, collection_name):
    """Generate colleciton connection to Mongodb"""
#Need to add where you cannot create raw data to the web app collection

    try:
        db = client[database]
    except Exception as e:
        print(f"Invalid database name, error: {e}")
    
    try:
        collection = db[collection_name]
        return collection
    
    except Exception as err:
        print(f"Error connecting to  collection {collection_name}, {err}")
        print(f"Did you mean one of the following: {[collection for collection in db.collection_names()]}")


    return collection 

def load_posts(posts, collection):
    """Load posts to Mongodb"""
    if posts:
        json_posts = posts.json()["data"]["children"]
        collection.insert_many(json_posts)
        print(f"Inserted {len(json_posts)} reddit posts to the collection")

def main(params):
    """Main function to extract Reddit posts and Load to temp collection"""

    #User Params
    db = params.db
    collection = params.coll
    subreddit = params.sub
    
    #Extract
    headers = get_access_token()
    posts = get_subreddit_data(subreddit, headers)

    #Load
    client = mongo_connection()
    collection = select_collection(client, db, collection)
    load_posts(posts, collection)


if __name__=='__main__':
    parser = argparse.ArgumentParser(description="Extract data from county website")
    parser.add_argument('--db', required=True, help="Mongodb database name")
    parser.add_argument('--coll', required=True, help="Mongodb collection name")
    parser.add_argument('--sub', required=True, help="Subreddit name")
    
    params = parser.parse_args()
    main(params)