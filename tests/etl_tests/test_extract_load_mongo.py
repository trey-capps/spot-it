"""python -m pytest etl_models_test/test_extract_load_mongo.py"""
from etl_models.extract_load_mongo import ExtractLoadMongo
from .... import config

# Method - mongo_connect()

def test_mongo_connect_invalid_db_str():
    """Inaccurate mongo string"""
    cred = config.mongo_cred
    mongo_connect = ExtractLoadMongo(cred + 'a', "TempPosts", "CollectRaw")
    assert mongo_connect.mongo_connect()

"""database not present"""

"""collection not present"""


#Method - filter_subreddit_posts(subreddit)



#Method - upload_subreddit_posts(posts)