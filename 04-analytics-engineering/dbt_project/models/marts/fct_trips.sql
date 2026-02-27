/*
To Do:
- One row per trip (doesn't matter if yellow or green)
- Add a primary key (trip_id). It has to be unique.
- Find all the duplicates, understand why they happen, and fix them.
- Find a way to enrich the column payment_type.
*/

WITH payment_types AS (
    SELECT
        *
    FROM {{ ref('dim_payment_types') }}
),

trips_dedup AS (
    SELECT 
        *
    FROM {{ ref("int_trips_unioned") }}
    GROUP BY 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19
), 

trips AS (
    SELECT 
        CONCAT(pickup_location_id, '-', dropoff_location_id, '-', pickup_datetime, '-', dropoff_datetime, '-', trip_distance, '-', passenger_count, '-', COALESCE(trip_type, 0), '-', total_amount) AS trip_id,
        d.*,
        p.payment_description
    FROM trips_dedup d LEFT JOIN payment_types p ON d.payment_type = p.payment_type
)

SELECT 
    *
FROM trips