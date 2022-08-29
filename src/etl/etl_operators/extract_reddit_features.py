class RedditFeatures:
    
    def __init__(self, data_field):
        self.data_field = data_field
        self.name = self.data_field["name"]
        self.title = self.data_field["title"]
        self.num_comments = self.data_field["num_comments"]
        self.ups = self.data_field["ups"]
        self.upvote_ratio = self.data_field["upvote_ratio"]
        self.created = self.data_field["created"]
        self.url = self.data_field["url"]
        self.subreddit = self.data_field["subreddit"]

    def extract_all_features(self):
        """Subset the Reddit features of interest"""
        filter_data = {
            "name": self.name,
            "title": self.title,
            "num_comments": self.num_comments,
            "ups": self.ups,
            "upvote_ratio": self.upvote_ratio,
            "created": self.created,
            "url": self.url,
            "subreddit": self.subreddit
        }
        
        return filter_data