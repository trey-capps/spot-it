import config
import pymongo
import pandas as pd

def main():
    client = pymongo.MongoClient(config.mongo_cred)

    db = client['RedditCollect']
    collection = db['indieheads']
    collect = db.list_collection_names()
    print(f'Here are the collections {collect}')
    cursor = collection.find({})
    reddit_df = pd.DataFrame(list(cursor))

    reddit_df.to_csv('test.csv', index = False)
    print('Exported CSV correctly')

if __name__=='__main__':
    main()