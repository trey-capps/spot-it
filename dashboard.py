"""
This file is used to create a streamlit dashboard
"""

import streamlit as st
import pandas as pd
from data_collection.spotify_collect import list_playlist, get_song, extract_song_data
from recommendation_models.cosine_similarity import generate_similar_songs, top_n_songs
import pymongo
import spotipy 
import plotly.express as px
import etl.config as config
from datetime import datetime

#Setup Database connection
def init_connection():
    return pymongo.MongoClient(config.mongo_cred)

client = init_connection()

def get_collection():
    db = client['RedditCollect']
    items = db.list_collection_names()
    return items

collections = get_collection()

st.set_page_config(
     page_title="Spot-It",
     layout="wide")

st.title('Spot-It (Version 1)')
with st.expander("About"):
    col1_0, col1_1 = st.columns(2)
    
    with col1_0:
        #Insert image
        st.write("[insert image here]")
    with col1_1:
        st.write("""
                This dashboard allows users to discover new music on Reddit.
                The first section gives you a weekly recape of the most popular
                and recent songs of the specified subreddit. The second section
                allows you to use your own Spotify playlist data to gain more specific
                song suggestions. 
            
                Link to code: https://github.com/trey-capps/spot-it

                Link to post: https://treycapps.com/posts/spotify_reddit

                Main tools used to create this project: Spotify API, Reddit API, Streamlit, MongoDB, 
                Scikit-learn, and Pandas 
            """)

#Add whitespace
st.header(" ")

subreddit_selection = st.selectbox(
        'To Begin, Select A Subreddit.',
        collections
    )
st.write('Future Subreddits Will Be Added!')

def collection_data(sub_select):
    db = client['RedditCollect']
    collection = db[sub_select]
    items = collection.find({})
    items = list(items)
    return items

subreddit_data = collection_data(subreddit_selection)
reddit_data = pd.DataFrame(list(subreddit_data))
reddit_data.rename(columns = {
    'artist_all': 'Artist(s)', 
    'track': 'Track', 
    'upvotes': 'Upvotes'},
    inplace = True)
with st.container():
    st.header("Past Week's Vibe For r/{}".format(subreddit_selection))

    col2_0, col2_1 = st.columns([1, 3])

    with col2_0:
        sub_choice = st.selectbox(
            "",
            ["Newly Posted","Most Upvoted"]
        )
    
        
    with col2_1:
        n = 5
        top_cols = ['Artist(s)','Track','Upvotes']
        if sub_choice == 'Most Upvoted':
            st.subheader("{} Most Upvoted Songs".format(n))
            df_top = reddit_data[top_cols].sort_values(by='Upvotes', ascending=False)
        if sub_choice == 'Newly Posted':
            st.subheader("{} Newly Posted Songs".format(n))
            df_top = reddit_data.sort_values(by='created', ascending=False)
            df_top = df_top[top_cols]
        df_top_n = df_top.head(n).set_index(pd.Series([x for x in range(1,n+1)]))
        st.table(df_top_n)
    
    #Plots
    track_features = ['danceability','energy','speechiness','acousticness','instrumentalness','valence']
    df_track_features = reddit_data[track_features]
    df_plot = df_track_features.mean(axis=0, )
    r = list(df_plot)
    fig = px.line_polar(df_plot, r=r, theta=track_features, line_close=True)
    fig.update_traces(fill='toself')
    st.plotly_chart(fig, use_container_width=True)
    

with st.container():
    st.header('For A More Personalized Experience, Enter Your Spotify Username!')
    st.write("By entering your Spotify username, you are agreeing to use your public Spotify playlist data for this dashboard.")
    user_name = st.text_input('Enter your Spotify Username: ')
    if user_name:
        st.subheader("Welcome {}!".format(user_name))
        try:
            user_playlist = list_playlist(user_name)
            list_of_playlist = list(user_playlist.keys())
            if len(list_of_playlist) == 0: 
                st.write('No public playlits found for {}'.format(user_name))
            
            #Allow user to select one of their playlists
            playlist_selection = st.selectbox(
                'Select A Public Playlist',
                list_of_playlist, 
            )
            
            #Get the URI of the user selected playlist
            playlist_selection_uri = user_playlist[playlist_selection]
            #Get songs based on selected playlist
            user_songs = get_song(playlist_selection_uri, artist = True)
            #Song data for the users selected playlist
            for song in user_songs:
                song.update(extract_song_data(song['track_id']))
                
            #Create Dataframe for all songs in playlist
            user_playlist_df = pd.DataFrame(user_songs, columns = track_features)
            
            #Create Vibe
            #A better metric can be derived in the future
            vibe = user_playlist_df.agg('mean').to_frame()
            
            similar_songs = generate_similar_songs(reddit_data, vibe, track_features)

            col3_0, col3_1 = st.columns([1, 3])

            with col3_0:
                n_choice = st.selectbox(
                    "Select the number of songs to generate.",
                    [5, 10, 15]
                )
    
        
            with col3_1:
                
                st.subheader("{0} Songs from r/{1} that are similar to {2}".format(n_choice, subreddit_selection, playlist_selection))
                
                recommended_songs = top_n_songs(similar_songs, n_choice)
                st.table(recommended_songs)
    

        except spotipy.SpotifyException:
            st.write('{} is not a valid Spotify username.'.format(user_name))

#White Space
st.title(' ')

#Create feedback form
used_tool = st.selectbox("Did you use the personalized tool?", [' ', 'Yes', 'No'])
if used_tool == "Yes":
    #Connect Feedback database, toolRating Collection
    rating_db = client['Feedback']
    rating_collection = rating_db['toolRating']
    with st.form(key = "tool_rating", clear_on_submit = True):
        st.write("Please rate the quality of the songs recommended by this tool. (1 = Not Good, 10 = Amazing)")
        st.write("This data will be used to improve model quality in the future.")

        rating = st.slider(" ", 1, 10)
        sub_suggest = st.text_input('What subreddit would you like to see added in the future?', '')

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit Feedback")
        if submitted:
            user_rating = {'_id': datetime.now(), 'rating': rating, 'sub_suggest': sub_suggest}
            rating_collection.insert_one(user_rating)
            st.write("Thanks for the feedback! More improvements coming soon!")
elif used_tool == "No":
    st.write(':(')