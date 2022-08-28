# Spot-it (In Progress)
A tool to find Reddit songs that may be a good fit for your Spotify playlist

Version 1 has been completed and the demo can be found here: https://youtu.be/dDmbO5_ccEc. Version 2 in the works!

## ETL Outline
```src/etl``` contains all the directories and files for the data collection process

#### Extract - Subreddit Raw posts
```ingest_reddit_raw.py``` is a python script that will collect the raw data from any subreddit and upload it to the ```temp_data``` staging directory

Example to scrape 25 new posts from r/indieheads: ```python ingest_reddit_raw.py --subreddit="indieheads"``` 

#### Transformation - Normalize Subreddit Posts and Filter Tracks
```extract_reddit_tracks.py``` is a python script that will clean (keep only important features from the API request) and extract the song posts from the raw posts found in ```temp_data``` for all subreddits detected in the raw scrape file

Example to clean and filter songs: ```python transform_reddit_posts.py```

#### Extraction - Spotify Audio Features
```extract_spotify_features.py``` is a script that takes in the clean, extracted track data for all the subreddits and add audio features from Spotify to these tracks. 

Example to add audio features: ```python extract_spotify_features.py```

#### ETL Models
This directory contains any custom classes that are useful for the ETL process

#### Next Steps
- Set up Airflow
    - Use the bash commands with the BashOperator to orchestrate the "E" and "T" tasks I currently have
- Add more subreddits

## Recommendation Models
This directory contains models used to generate similarity metrics for songs. More methods have been explored. Unsupervised model techniques have been explored in the ```src/recommendation_models``` directory. When the ETL pipeline and data warehouse is complete more robust recommendation models will be developed.

## API Creation
This directory contains the basic files to develop a RESTful API. This will be expanded when the data collection is complete. This API will be first be available to request songs (and respective data points) for certain subreddits. The second phase will allow users to send requests to generate song recommendations. This will also aid in the future development of the frontend application.

# Version 1 Dashboard
Version 1 has been completed and the demo can be found here: https://youtu.be/dDmbO5_ccEc.