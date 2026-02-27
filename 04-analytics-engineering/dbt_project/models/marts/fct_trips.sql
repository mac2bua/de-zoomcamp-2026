{{ config(materialized='incremental', unique_key='trip_id', incremental_strategy='merge', on_schema_change='append_new_columns') }}

-- Fact table containing all taxi trips enriched with zone information
-- This is a classic star schema design: fact table (trips) joined to dimension table (zones)
-- Materialized incrementally to handle large datasets efficiently

WITH trips_with_payment AS (
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
        -- Trip identifiers
        vendor_id,
        'Green' as service_type,  -- Will be updated when we add yellow trips properly
        rate_code_id,
        
        -- Location details
        pickup_location_id,
        dropoff_location_id,
        
        -- Trip timing
        pickup_datetime,
        dropoff_datetime,
        store_and_fwd_flag,
        
        -- Trip metrics
        passenger_count,
        trip_distance,
        trip_type,
        
        -- Payment breakdown
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
)

SELECT
    t.trip_id,
    t.vendor_id,
    t.service_type,
    t.rate_code_id,
    
    -- Location details (enriched with human-readable zone names from dimension)
    t.pickup_location_id,
    pz.borough as pickup_borough,
    pz.zone as pickup_zone,
    t.dropoff_location_id,
    dz.borough as dropoff_borough,
    dz.zone as dropoff_zone,
    
    -- Trip timing
    t.pickup_datetime,
    t.dropoff_datetime,
    t.store_and_fwd_flag,
    
    -- Trip metrics
    t.passenger_count,
    t.trip_distance,
    t.trip_type,
    TIMESTAMP_DIFF(t.dropoff_datetime, t.pickup_datetime, MINUTE) as trip_duration_minutes,
    
    -- Payment breakdown
    t.fare_amount,
    t.extra,
    t.mta_tax,
    t.tip_amount,
    t.tolls_amount,
    t.ehail_fee,
    t.improvement_surcharge,
    t.total_amount,
    t.payment_type,
    p.payment_description as payment_type_description

FROM trips_with_payment t

-- LEFT JOIN preserves all trips even if zone information is missing or unknown
LEFT JOIN {{ ref('dim_zones') }} as pz ON t.pickup_location_id = pz.location_id
LEFT JOIN {{ ref('dim_zones') }} as dz ON t.dropoff_location_id = dz.location_id
LEFT JOIN {{ ref('dim_payment_types') }} as p ON t.payment_type = p.payment_type

{% if is_incremental() %}
    -- Only process new trips based on pickup datetime
    WHERE t.pickup_datetime > (SELECT MAX(pickup_datetime) FROM {{ this }})
{% endif %}
