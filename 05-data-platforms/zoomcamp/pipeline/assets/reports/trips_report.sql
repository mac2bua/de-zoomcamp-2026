/* @bruin

name: reports.trips_report
type: duckdb.sql

depends:
  - staging.trips

materialization:
  type: table
  strategy: time_interval
  incremental_key: pickup_datetime
  time_granularity: timestamp

columns:
  - name: pickup_date
    type: date
    description: Date of pickup
    primary_key: true
  - name: fleet_type
    type: string
    description: Taxi fleet type
    primary_key: true
  - name: total_trips
    type: bigint
    description: Total number of trips
    checks:
      - name: non_negative
  - name: total_passengers
    type: bigint
    description: Total passengers
    checks:
      - name: non_negative
  - name: total_distance
    type: float
    description: Total trip distance
    checks:
      - name: non_negative
  - name: total_fare
    type: float
    description: Total fare amount
    checks:
      - name: non_negative

@bruin */

-- Reports: aggregate by date, fleet_type, and payment type
SELECT 
    DATE(pickup_datetime) AS pickup_date,
    fleet_type,
    COUNT(*) AS total_trips,
    SUM(passenger_count) AS total_passengers,
    SUM(trip_distance) AS total_distance,
    SUM(fare_amount) AS total_fare
FROM staging.trips
WHERE pickup_datetime >= '{{ start_datetime }}'
  AND pickup_datetime < '{{ end_datetime }}'
GROUP BY 
    DATE(pickup_datetime),
    fleet_type
