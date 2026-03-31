import json
import pandas as pd
from kafka import KafkaProducer
from time import time

# Read parquet file
df = pd.read_parquet('data/green_tripdata_2025-10.parquet')

# Keep only required columns
columns = [
    'lpep_pickup_datetime',
    'lpep_dropoff_datetime',
    'PULocationID',
    'DOLocationID',
    'passenger_count',
    'trip_distance',
    'tip_amount',
    'total_amount'
]
df = df[columns]

# Convert datetime columns to strings
df['lpep_pickup_datetime'] = df['lpep_pickup_datetime'].astype(str)
df['lpep_dropoff_datetime'] = df['lpep_dropoff_datetime'].astype(str)

# Create Kafka producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Send all rows
t0 = time()

for _, row in df.iterrows():
    message = row.to_dict()
    producer.send('green-trips', value=message)
    producer.flush()  # Ensure message is sent

t1 = time()
print(f'Took {(t1 - t0):.2f} seconds')
