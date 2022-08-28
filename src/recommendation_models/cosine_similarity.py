import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def generate_similar_songs(reddit_songs, vibe, track_features):
    '''
    reddit_songs (pandas DataFrame): songs in the selected subreddit
    vibe (numpy arrary): array of vibe metric
    track_features (list): list of track features selected for the analysis
    
    Output:
    Pandas DataFrame with 'cosine_sim' (cosine similarity metric) generated 
    and appended to original DataFrame
    '''

    reddit_features = reddit_songs[track_features]
    reddit_array = reddit_features.to_numpy()
    cos_sim = []
    for track in reddit_array:
        similarity = cosine_similarity(np.array([track]), vibe.T.to_numpy())
        cos_sim.append(similarity)
    
    #Append back to dataframe
    #Flatten nested array/list
    reshape_cos_sim = [ar[0, 0] for ar in cos_sim]
    reddit_songs['cosine_sim'] = reshape_cos_sim

    #Export dataframe
    return reddit_songs


def top_n_songs(cos_sim_df, top_num):
    
    #export the dataframe
    cos_sim_df.sort_values(by = 'cosine_sim', ascending = False, inplace = True)
    top_n = cos_sim_df.head(top_num)
    top_n = top_n[['Artist(s)', 'Track', 'Upvotes']]
    new_index = pd.Series([x for x in range(1, top_num+1)])
    top_n.set_index(new_index, inplace = True)
    return top_n