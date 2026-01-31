#!/usr/bin/env python
# coding: utf-8

import click
import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm


dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

@click.command()
@click.option('--url', default=None, help='URL of the parquet file to ingest')
@click.option('--pg-user', default='postgres', help='PostgreSQL user')
@click.option('--pg-pass', default='postgres', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default='5433', help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database')
@click.option('--target-table', default='green_taxi_data', help='Target table name')
@click.option('--chunksize', default=100000, help='Chunk size for data ingestion')
def run(url, pg_user, pg_pass, pg_host, pg_port, pg_db, target_table, chunksize):
    """Ingest data into PostgreSQL database in chunks."""

    # Connect to postgresql running as a docker container
    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')
    print("Connected to the database")

    # Ingest taxi data
    if url is None:
        url = "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet"

    df = pd.read_parquet(url)
    print("Started ingesting Green Taxi Data")

    df.to_sql(name=target_table, con=engine, if_exists="replace")
    print("Green Taxi Data ingestion completed")

    # Ingest taxi zone lookup data
    url_zones = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv'
    df_zones = pd.read_csv(url_zones)
    print("Started ingesting Taxi Zone Lookup Data")

    df_zones.to_sql(name='taxi_zone_lookup', con=engine, if_exists="replace")
    print("Taxi zone lookup table created")

if __name__ == "__main__":
    run()




