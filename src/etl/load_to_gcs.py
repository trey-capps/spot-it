from datetime import date
from google.cloud import storage
import config

#TODO: Convert json to csv for easier load into BQ

#Variables imported from Terrafrom 
CRED_PATH = config.gcp_auth_file_path
BUCKET_NAME = config.gcp_bucket_name

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """
    Uploads a file to the bucket
    (Directly from GCP documentation)
    """
    #Specify to use the Terraform service account keys
    storage_client = storage.Client.from_service_account_json(CRED_PATH)
    
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)

    print(f"File {source_file_name} uploaded to {destination_blob_name}.")

def main():
    #Can eventually make these user params for future functionality
    bucket_name = BUCKET_NAME
    source_file_name = f"./temp_data/{date.today()}_clean_features.json"
    destination_blob_name = f"{date.today()}_spotify_reddit.json"

    try:
        upload_blob(bucket_name, source_file_name, destination_blob_name)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()