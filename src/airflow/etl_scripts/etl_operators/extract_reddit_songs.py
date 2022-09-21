from etl_operators.extract_reddit_features import RedditFeatures
from typing import Dict

class ExtractSong(RedditFeatures):
    
    def __init__(self, data_field: Dict) -> None:
        super().__init__(data_field)
    
    def is_track(self) -> bool:
        """Determine if post title is a track""" 
        return '-' in self.title
    
    def extract_track(self) -> None:
        """Parse the 'track' from the post title"""
        pass

    def extract_artist(self) -> None:
        """Parse the 'artist' from the post title"""
        pass