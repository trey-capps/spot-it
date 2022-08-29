import pymongo

class ExtractLoadMongo:
    
    def __init__(self, mongo_string, db_name, collection_name):
        self.mongo_string = mongo_string
        self.db_name = db_name
        self.collection_name = collection_name

    def mongo_client(self):
        """Establish connection with MongoDB using connection string"""
        try:
            return pymongo.MongoClient(self.mongo_string)
        except Exception as e:
            print(f"Error with client connection: {e}")
            return None
            
    def mongo_database(self):
        """Create Mongo database instance"""
        client = self.mongo_client()
        return client[self.db_name]
        
    def mongo_collection(self):
        """Create Mongo collection instance"""
        db = self.mongo_database()
        return db[self.collection_name]
        
    def filter_subreddit_posts(self, subreddit):
        """
        Subset Mongo data based on a subreddit of interest
        subreddit (str): subreddit name 
        """
        try:
            collection = self.mongo_collection()
            cursor = collection.find({ "data.subreddit" : subreddit })
            subreddit_posts = list(cursor)
            return subreddit_posts
        except AttributeError:
            print("Collection not found, use the mongo_connect() method before you filter posts")
            return None
    
    def upload_data(self, posts):
        """
        Upload data to Mongo
        posts (list): list of documents to be uploaded
        """
        duplicate = []
        for post in posts:
            try:
                collection = self.mongo_collection()
                collection.insert_one(post)
            except pymongo.errors.DuplicateKeyError:
                duplicate.append(1)
    
        print('{0} records were not added becasue they are duplicates'.format(len(duplicate)))
    
    def select_track_artist(self):
        """Select only the documents containing 'track' and 'artists'"""
        try:
            collection = self.mongo_collection()
            cursor = collection.find({}, {'artist': 1,  'track': 1})
            track_artist = list(cursor)
            return track_artist
        except AttributeError:
            print("Collection not found, use the mongo_client() method before you filter posts")
            return None

    def drop_data(self):
        pass