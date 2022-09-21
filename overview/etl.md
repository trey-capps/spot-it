# ETL Outline

```src/etl``` contains all the directories and files for the data collection process

## ETL Class Modules
```etl/etl_operators``` contains custom classes to abstract out API calls and Mongo functionality.

## Steps in Initial Pipeline

Change to the ```etl``` directory:

``` cd ./src/etl ```

### Extract - Subreddit Raw posts
```ingest_reddit_raw.py``` is a python script that will collect the raw data from any subreddit and upload it to the ```temp_data``` staging directory

Example to scrape 25 new posts from r/indieheads: 

```python ingest_reddit_raw.py --subreddit="indieheads"``` 

### Transformation - Normalize Subreddit Posts and Filter Tracks
```extract_reddit_tracks.py``` is a python script that will clean (keep only important features from the API request) and extract the song posts from the raw posts found in ```temp_data``` for all subreddits detected in the raw scrape file

Example to clean and filter songs: 

```python transform_reddit_posts.py```

### Extraction - Spotify Audio Features
```extract_spotify_features.py``` is a script that takes in the clean, extracted track data for all the subreddits and add audio features from Spotify to these tracks. 

Example to add audio features: 

```python extract_spotify_features.py```

### Load - Load to Google cloud storage
```load_to_gcs.py``` is a script that loads the cleaned and aggregated subreddit tracks with their audio features to Google cloud storage. This storage bucket serves as the landing zone for daily (or other frequency) scrapes.

Example to upload to cloud storage:

```python load_to_gcs.py``` 

### Next Steps
- Finish setting up Airflow
- Setup Big Query so each days data can be aggregated into a DW



## Airflow Setup via Docker

All steps to setup Airflow come straight from the offical documentation found [here](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html).

### Fetch the docker-compose.yaml

```
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.4.0/docker-compose.yaml'
```
### Setup Environment

#### File Directory With root User Ownership

```mkdir -p ./logs ./plugins```
```echo -e "AIRFLOW_UID=$(id -u)" > .env```

#### Initialize Airflow Database

```docker-compose up airflow-init```

Login and password are both 'airflow' by default

### Run Airflow

```docker-compose up```

### Airflow UI 

```http://localhost:8080``` using username and password from [initialization](#initialize-airflow-database)

---