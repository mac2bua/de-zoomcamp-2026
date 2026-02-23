import os
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from google.cloud import storage
from google.api_core.exceptions import NotFound, Forbidden
import time


# Change this to your bucket name
BUCKET_NAME = "dezoomcamp-hw4-2026-mac2bua"

# Path to your GCP credentials (put in same folder as this script or use absolute path)
# IMPORTANT: Never commit this file to Git!
CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), "gcs.json")

# Try to load credentials, fallback to default gcloud auth
if os.path.exists(CREDENTIALS_FILE):
    client = storage.Client.from_service_account_json(CREDENTIALS_FILE)
else:
    # Use default credentials from gcloud
    client = storage.Client()


# Data configuration
TAXI_TYPES = ["green", "yellow", "fhv"]
YEARS = {
    "green": ["2019", "2020"],
    "yellow": ["2019", "2020"],
    "fhv": ["2019"]  # FHV only has 2019
}
MONTHS = [f"{i:02d}" for i in range(1, 13)]  # 1-12

BASE_URL = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/"
DOWNLOAD_DIR = "./data"

CHUNK_SIZE = 8 * 1024 * 1024

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

bucket = client.bucket(BUCKET_NAME)


def download_file(args):
    """Download a single file. Args is a tuple of (taxi_type, year, month)"""
    taxi, year, month = args
    url = f"{BASE_URL}{taxi}/{taxi}_tripdata_{year}-{month}.csv.gz"
    file_path = os.path.join(DOWNLOAD_DIR, f"{taxi}_tripdata_{year}-{month}.csv.gz")

    try:
        print(f"Downloading {url}...")
        urllib.request.urlretrieve(url, file_path)
        print(f"Downloaded: {file_path}")
        return file_path
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None


def create_bucket(bucket_name):
    try:
        bucket = client.get_bucket(bucket_name)
        project_bucket_ids = [bckt.id for bckt in client.list_buckets()]
        if bucket_name in project_bucket_ids:
            print(f"Bucket '{bucket_name}' exists and belongs to your project. Proceeding...")
        else:
            print(f"Bucket '{bucket_name}' exists but doesn't belong to your project.")
            sys.exit(1)
    except NotFound:
        bucket = client.create_bucket(bucket_name)
        print(f"Created bucket '{bucket_name}'")
    except Forbidden:
        print(f"Bucket '{bucket_name}' exists but is not accessible.")
        sys.exit(1)


def verify_gcs_upload(blob_name):
    return storage.Blob(bucket=bucket, name=blob_name).exists(client)


def upload_to_gcs(file_path, max_retries=3):
    if file_path is None:
        return
    
    blob_name = os.path.basename(file_path)
    blob = bucket.blob(blob_name)
    blob.chunk_size = CHUNK_SIZE

    for attempt in range(max_retries):
        try:
            print(f"Uploading {file_path} to {BUCKET_NAME} (Attempt {attempt + 1})...")
            blob.upload_from_filename(file_path)
            print(f"Uploaded: gs://{BUCKET_NAME}/{blob_name}")

            if verify_gcs_upload(blob_name):
                print(f"Verification successful for {blob_name}")
                return
            else:
                print(f"Verification failed for {blob_name}, retrying...")
        except Exception as e:
            print(f"Failed to upload {file_path} to GCS: {e}")

        time.sleep(5)

    print(f"Giving up on {file_path} after {max_retries} attempts.")


if __name__ == "__main__":
    create_bucket(BUCKET_NAME)

    # Create list of all files to download
    download_tasks = []
    for taxi in TAXI_TYPES:
        for year in YEARS.get(taxi, []):
            for month in MONTHS:
                download_tasks.append((taxi, year, month))

    print(f"Total files to download: {len(download_tasks)}")

    # Download all files in parallel
    with ThreadPoolExecutor(max_workers=4) as executor:
        file_paths = list(executor.map(download_file, download_tasks))

    # Upload all files in parallel
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(upload_to_gcs, file_paths)

    print("All files processed and verified.")
