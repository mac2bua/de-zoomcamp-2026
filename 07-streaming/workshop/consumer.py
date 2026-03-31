from kafka import KafkaConsumer
import json

# Create consumer
consumer = KafkaConsumer(
    'green-trips',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    consumer_timeout_ms=10000,  # Stop after 10 seconds of no messages
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

# Count trips with distance > 5
count = 0
for message in consumer:
    trip = message.value
    if trip['trip_distance'] > 5.0:
        count += 1

print(f'Trips with distance > 5: {count}')
