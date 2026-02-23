"""
Quick script to download and upload ONLY FHV 2019 data to GCS.
"""

import os
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from google.cloud import storage
import time


BUCKET_NAME = "dezoomcamp-hw4-2026-mac2bua"

# Credentials - update path if needed
CREDENTIALS_FILE = "gcs.json"

if os.path.exists(CREDENTIALS_FILE):
    client = storage.Client.from_service_account_json(CREDENTIALS_FILE)
else:
    client = storage.Client()

bucket = client.bucket(BUCKET_NAME)

BASE_URL = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/"
DOWNLOAD_DIR = "./fhv_download"
CHUNK_SIZE = 8 * 1024 * 1024

os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def download_fhv(year, month):
    url = f"{BASE_URL}fhv/fhv_tripdata_{year}-{month:02d}.csv.gz"
    filepath = os.path.join(DOWNLOAD_DIR, f"fhv_tripdata_{year}-{month:02d}.csv.gz")
    
    try:
        print(f"Downloading {url}...")
        urllib.request.urlretrieve(url, filepath)
        print(f"Downloaded: {filepath}")
        return filepath
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None


def upload_to_gcs(filepath):
    if filepath is None:
        return
    
    blob_name = os.path.basename(filepath)
    blob = bucket.blob(blob_name)
    blob.chunk_size = CHUNK_SIZE
    
    try:
        print(f"Uploading {filepath} to {BUCKET_NAME}...")
        blob.upload_from_filename(filepath)
        print(f"Uploaded: gs://{BUCKET_NAME}/{blob_name}")
    except Exception as e:
        print(f"Failed to upload {filepath}: {e}")


if __name__ == "__main__":
    # Only FHV 2019
    tasks = [("2019", m) for m in range(1, 13)]
    
    print(f"Downloading {len(tasks)} FHV files...")
    
    # Download in parallel
    with ThreadPoolExecutor(max_workers=4) as executor:
        files = list(executor.map(lambda t: download_fhv(t[0], t[1]), tasks))
    
    # Upload in parallel
    with ThreadPoolExecutor(max_workers=4) as executor:
        list(executor.map(upload_to_gcs, files))
    
    print("Done!")
