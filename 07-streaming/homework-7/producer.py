import json
import pandas as pd
from kafka import KafkaProducer
from time import time
from models import ride_serializer, ride_from_row

# Read parquet file
df = pd.read_parquet('data/green_tripdata_2025-10.parquet')

# Keep only required columns
columns = [
    'PULocationID',
    'DOLocationID',
    'trip_distance',
    'total_amount',
    'tip_amount',
    'lpep_pickup_datetime'
]
df = df[columns]

# Convert datetime columns to strings
df['lpep_pickup_datetime'] = df['lpep_pickup_datetime'].astype(str)

# Create Kafka producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=ride_serializer
)

# Send all rows
t0 = time()

for _, row in df.iterrows():
    message = row.to_dict()
    ride = ride_from_row(message)
    producer.send('green-trips', value=ride)
    producer.flush()  # Ensure message is sent

t1 = time()
print(f'Took {(t1 - t0):.2f} seconds')
