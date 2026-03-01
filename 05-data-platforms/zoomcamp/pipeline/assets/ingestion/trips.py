"""@bruin

name: ingestion.trips

type: python
image: python:3.11
connection: duckdb-default

materialization:
  type: table
  strategy: append

columns:
  - name: trip_id
    type: integer
    description: Unique identifier for each trip record
    primary_key: true
  - name: vendor_id
    type: string
    description: Identifier for the vendor (e.g. 'CMTV' for Creative Mobile)
  - name: pickup_datetime
    type: timestamp
    description: Timestamp when the taxi was picked up
  - name: dropoff_datetime
    type: timestamp
    description: Timestamp when the taxi was dropped off
  - name: passenger_count
    type: integer
    description: Number of passengers in the taxi at pickup
  - name: trip_distance
    type: float
    description: Distance traveled during the trip
  - name: ratecode_id
    type: string
    description: Rate code identifier (e.g. '1' for Standard rate)
  - name: store_and_fwd_flag
    type: string
    description: Flag indicating whether the trip was stored and forwarded
  - name: pickup_location_id
    type: integer
    description: Identifier for the pickup location
  - name: dropoff_location_id
    type: integer
    description: Identifier for the dropoff location
  - name: fleet_type
    type: string
    description: Type of taxi fleet (e.g. 'yellow', 'green')

@bruin"""

import os
import io
import pandas as pd
import requests
from datetime import datetime
import json


def materialize():
    # Get runtime context from environment variables
    start_date = os.environ.get('BRUIN_START_DATE', '2022-01-01')
    end_date = os.environ.get('BRUIN_END_DATE', '2022-01-31')
    
    # Get pipeline variables
    bruin_vars = os.environ.get('BRUIN_VARS', '{}')
    variables = json.loads(bruin_vars)
    taxi_types = variables.get('taxi_types', ['yellow'])
    
    # NYC Taxi data URL base
    base_url = 'https://d37ci6vzurychx.cloudfront.net/trip-data/'
    
    all_data = []
    
    for taxi_type in taxi_types:
        # Generate URLs for each month in the range
        start_year = int(start_date[:4])
        start_month = int(start_date[5:7])
        end_year = int(end_date[:4])
        end_month = int(end_date[5:7])
        
        year = start_year
        month = start_month
        
        while (year < end_year) or (year == end_year and month <= end_month):
            # Format: yellow_tripdata_2022-01.parquet
            filename = f"{taxi_type}_tripdata_{year}-{month:02d}.parquet"
            url = f"{base_url}{filename}"
            
            print(f"Fetching: {url}")
            
            try:
                response = requests.get(url, timeout=30)
                if response.status_code == 200:
                    # Read parquet directly from bytes using pyarrow
                    df = pd.read_parquet(io.BytesIO(response.content))
                    
                    # Add fleet_type
                    df['fleet_type'] = taxi_type
                    
                    # Add unique trip_id (the parquet files don't have one)
                    df['trip_id'] = range(1, len(df) + 1)
                    
                    all_data.append(df)
                else:
                    print(f"File not found: {url}")
            except Exception as e:
                print(f"Error fetching {url}: {e}")
            
            # Move to next month
            month += 1
            if month > 12:
                month = 1
                year += 1
    
    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        
        # Add extracted_at timestamp
        final_df['extracted_at'] = datetime.now()
        
        return final_df
    else:
        # Return empty DataFrame with expected schema
        return pd.DataFrame(columns=[
            'trip_id', 'vendor_id', 'pickup_datetime', 'dropoff_datetime',
            'passenger_count', 'trip_distance', 'ratecode_id',
            'store_and_fwd_flag', 'pickup_location_id', 'dropoff_location_id',
            'fleet_type', 'extracted_at'
        ])
