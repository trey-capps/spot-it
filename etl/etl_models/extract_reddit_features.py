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
        filter_data = {}
        filter_data["name"] = self.name
        filter_data["title"] = self.title
        filter_data["num_comments"] = self.num_comments
        filter_data["ups"] = self.ups
        filter_data["upvote_ratio"] = self.upvote_ratio
        filter_data["created"] = self.created
        filter_data["url"] = self.url
        filter_data["subreddit"] = self.subreddit

        return filter_data