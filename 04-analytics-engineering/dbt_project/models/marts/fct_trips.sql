/*
To Do:
- One row per trip (doesn't matter if yellow or green)
- Add a primary key (trip_id). It has to be unique.
- Find all the duplicates, understand why they happen, and fix them.
- Find a way to enrich the column payment_type.
*/

WITH trips AS (
    SELECT 
        -- Create unique trip_id from key trip attributes
        CONCAT(
            CAST(pickup_location_id AS STRING), '-',
            CAST(dropoff_location_id AS STRING), '-',
            CAST(pickup_datetime AS STRING), '-',
            CAST(dropoff_datetime AS STRING), '-',
            CAST(trip_distance AS STRING), '-',
            CAST(passenger_count AS STRING), '-',
            CAST(COALESCE(trip_type, 0) AS STRING), '-',
            CAST(total_amount AS STRING)
        ) AS trip_id,
        vendor_id,
        rate_code_id,
        pickup_location_id,
        dropoff_location_id,
        pickup_datetime,
        dropoff_datetime,
        store_and_fwd_flag,
        passenger_count,
        trip_distance,
        trip_type,
        fare_amount,
        extra,
        mta_tax,
        tip_amount,
        tolls_amount,
        ehail_fee,
        improvement_surcharge,
        total_amount,
        payment_type
    FROM {{ ref('int_trips_unioned') }}
),

trips_with_payment AS (
    SELECT 
        t.*,
        p.payment_description
    FROM trips t
    LEFT JOIN {{ ref('dim_payment_types') }} p 
        ON t.payment_type = p.payment_type
),

deduped AS (
    -- Remove exact duplicates, keeping one record per trip_id
    SELECT *,
        ROW_NUMBER() OVER (PARTITION BY trip_id) AS rn
    FROM trips_with_payment
)

SELECT 
    trip_id,
    vendor_id,
    rate_code_id,
    pickup_location_id,
    dropoff_location_id,
    pickup_datetime,
    dropoff_datetime,
    store_and_fwd_flag,
    passenger_count,
    trip_distance,
    trip_type,
    fare_amount,
    extra,
    mta_tax,
    tip_amount,
    tolls_amount,
    ehail_fee,
    improvement_surcharge,
    total_amount,
    payment_type,
    payment_description
FROM deduped
WHERE rn = 1