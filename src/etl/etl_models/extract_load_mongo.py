import pymongo

class ExtractLoadMongo:
    
    def __init__(self, mongo_string, db_name, collection_name):
        self.mongo_string = mongo_string
        self.db_name = db_name
        self.collection_name = collection_name

    def mongo_connect(self):
        
        client = pymongo.MongoClient(self.mongo_string)
        
        if self.db_name in client.list_databases():
            db = client[self.db_name]
        else:
            print(f"{self.db_name} does not exist, please enter a database from the following: {client.list_databases()}")
        
        if self.collection in db.list_collection_names():
            self.collection = db[self.collection_name]
        else:
            print(f"{self.collection_name} not in {self.db_name}")
        
    def filter_subreddit_posts(self, subreddit):
        try:
            cursor = self.collection.find({ "data.subreddit" : subreddit })
            subreddit_posts = list(cursor)
            return subreddit_posts
        except AttributeError:
            print("Collection not found, use the mongo_connect() method before you filter posts")
    
    def upload_data(self, posts):
        duplicate = []
        for post in posts:
            try:
                self.collection.insert_one(post)
            except pymongo.errors.DuplicateKeyError:
                duplicate.append(1)
    
        print('{0} records were not added becasue they are duplicates'.format(len(duplicate)))
    
    def drop_data(self):
        pass