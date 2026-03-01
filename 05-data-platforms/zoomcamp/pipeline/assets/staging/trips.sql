/* @bruin

name: staging.trips
type: duckdb.sql

depends:
  - ingestion.trips
  - ingestion.payment_lookup

materialization:
  type: table
  strategy: time_interval
  incremental_key: pickup_datetime
  time_granularity: timestamp

columns:
  - name: trip_id
    type: integer
    description: Unique trip identifier
    primary_key: true
    nullable: false
    checks:
      - name: not_null
  - name: vendor_id
    type: string
    description: Vendor identifier
  - name: pickup_datetime
    type: timestamp
    description: Pickup timestamp
    checks:
      - name: not_null
  - name: dropoff_datetime
    type: timestamp
    description: Dropoff timestamp
  - name: passenger_count
    type: integer
    description: Number of passengers
    checks:
      - name: non_negative
  - name: trip_distance
    type: float
    description: Trip distance in miles
    checks:
      - name: non_negative
  - name: ratecode_id
    type: string
    description: Rate code
  - name: store_and_fwd_flag
    type: string
    description: Store and forward flag
  - name: pickup_location_id
    type: integer
    description: Pickup location ID
  - name: dropoff_location_id
    type: integer
    description: Dropoff location ID
  - name: fleet_type
    type: string
    description: Taxi fleet type
  - name: payment_type
    type: integer
    description: Payment type
  - name: fare_amount
    type: float
    description: Fare amount
    checks:
      - name: non_negative
  - name: extracted_at
    type: timestamp
    description: Extraction timestamp

@bruin */

-- Staging: clean, deduplicate, and enrich raw data
WITH deduplicated AS (
    SELECT *,
        ROW_NUMBER() OVER (
            PARTITION BY trip_id 
            ORDER BY extracted_at DESC
        ) AS rn
    FROM ingestion.trips
    WHERE pickup_datetime >= '{{ start_datetime }}'
      AND pickup_datetime < '{{ end_datetime }}'
)
SELECT 
    d.trip_id,
    d.vendor_id,
    d.pup_datetime AS pickup_datetime,
    d.dropoff_datetime,
    d.passenger_count,
    d.trip_distance,
    d.ratecode_id,
    d.store_and_fwd_flag,
    d.pickup_location_id,
    d.dropoff_location_id,
    d.fleet_type,
    d.payment_type,
    d.fare_amount,
    d.extracted_at
FROM deduplicated d
WHERE d.rn = 1
  AND d.trip_id IS NOT NULL
  AND d.pickup_datetime IS NOT NULL
