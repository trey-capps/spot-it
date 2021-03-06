# Spot-it (In Progress)
A tool to find Reddit songs that may be a good fit for your Spotify playlist

## ETL Outline
The ETL directory contains all python files for the ETL process outlined below.

#### Ingest from Reddit
```ingest.py``` is a python script that will collect the raw data from any subreddit

#### ETL Models
Defined in the etl_models directory are custom class objects and methods that aid in the ETL process.
These objects will be incorporated in python scripts to take the raw data and eventually store the data into the production collection

```lake_to_staging.py``` is the first of many ETL scripts utilizing the custom classes created. 

To add song data to the staged Reddit posts, we can use the ```ExtractSpotify``` class found in ```src/etl/etl_models``` directory.

A script will be created to utilize the methods of this class.

#### Next Steps
- Integrating Spotify data into our subreddit data. 
- Automating the ETL process


## Recommendation Models
This directory contains models used to generate similarity metrics for songs. More methods have been explored. Unsupervised model techniques have been explored in the ```src/recommendation_models``` directory. When the ETL and data warehouse is complete more robust recommendation models will be developed.

## API Creation
This directory contains files to develop a RESTful API to support the future frontend development process

## dashboard.py
This file contains code to develop version 1 streamlit dashboard. This web application will be expanded upon when the ETL and data storage development process is complete.

# Final Dashboard
Version 1 has been completed and the demo can be found here: https://youtu.be/dDmbO5_ccEc