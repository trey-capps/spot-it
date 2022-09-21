from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

"""
DAG to extract reddit posts, clean, merge, and add Spotify audio features, and load to GCP
"""

#Add path to etl scripts
FILE_PATH_SCRIPTS = "./etl_scripts"

default_args = {
    "owner": "airflow", 
    "depends_on_past": False, 
    "retries": 1,
    "start_date": days_ago(0),
    }

with DAG(
    dag_id="etl_reddit_spotify",
    description="Spot-It ETL",
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False,
    max_active_runs=1,
) as dag:

    ingest_indieheads_raw_data = BashOperator(
        task_id="ingest_indieheads_raw_data",
        bash_command=f"python {FILE_PATH_SCRIPTS}/ingest_reddit_raw.py --subreddit='indieheads'",
        dag=dag,
    )
    
    ingest_Alternativerock_raw_data = BashOperator(
        task_id="ingest_Alternativerock_raw_data",
        bash_command=f"python {FILE_PATH_SCRIPTS}/ingest_reddit_raw.py --subreddit='Alternativerock'",
        dag=dag,
    )

    transform_reddit_posts = BashOperator(
        task_id="transform_reddit_posts",
        bash_command=f"python {FILE_PATH_SCRIPTS}/transform_reddit_posts.py",
        dag=dag,
    )

    extract_spotify_features = BashOperator(
        task_id="extract_spotify_features",
        bash_command=f"python {FILE_PATH_SCRIPTS}/extract_spotify_features.py",
        dag=dag,
    )

    load_to_gcs = BashOperator(
        task_id="upload_to_gcs",
        bash_command=f"python {FILE_PATH_SCRIPTS}/load_to_gcs.py",
        dag=dag,
    )

[ingest_indieheads_raw_data, ingest_Alternativerock_raw_data]  >> transform_reddit_posts >> extract_spotify_features >> load_to_gcs