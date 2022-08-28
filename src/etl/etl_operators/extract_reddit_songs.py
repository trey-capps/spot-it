from etl_operators.extract_reddit_features import RedditFeatures

class ExtractSong(RedditFeatures):
    
    def __init__(self, data_field):
        super().__init__(data_field)
    
    def is_track(self):
        return '-' in self.title
    
    def extract_track():
        pass

    def extract_artist():
        pass