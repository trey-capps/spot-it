from etl_operators.extract_reddit_songs import ExtractSong
import re

class ExtractIndieHeads(ExtractSong):
    
    def __init__(self, data_field):
        super().__init__(data_field)
        
    def is_track(self):
        result = (('[FRESH]' in self.title) and ('reddit' not in self.url))
        return result
    
    def extract_artist(self):
        artist_all = re.sub(r'\-(.*)', '', self.title)
        artist_all = artist_all.replace('[FRESH]', '')
        return artist_all.strip()
    
    def extract_track(self):
        track = re.sub(r'(.*)\-', '', self.title)
        return track.strip()


class ExtractAlternativeRock(ExtractSong):
    
    def __init__(self, title):
        super().__init__(title)
    
    def extract_artist(self):
        artist_all = re.sub(r'\-(.*)', '', self.title)
        return artist_all.strip()
    
    def extract_track(self):
        track = re.sub(r'(.*)\-', '', self.title)
        track = re.sub(r'[\(\[].*?[\)\]]', '', track)
        return track.strip()

#Subreddits to add:
# r/HipHopHeads
# r/popheads
# r/DubStep
# r/ElectronicMusic
# r/jazz