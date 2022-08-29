from etl_operators.extract_reddit_features import RedditFeatures

class ExtractSong(RedditFeatures):
    
    def __init__(self, data_field):
        super().__init__(data_field)
    
    def is_track(self):
        """Determine if post title is a track""" 
        return '-' in self.title
    
    def extract_track():
        """Parse the 'track' from the post title"""
        pass

    def extract_artist():
        """Parse the 'artist' from the post title"""
        pass