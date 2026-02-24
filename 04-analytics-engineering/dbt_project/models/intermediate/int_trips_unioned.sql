WITH green_tripdata AS (
    SELECT * FROM {{ ref('stg_green_tripdata') }}
),
WITH yellow_tripdata AS (
    SELECT * FROM {{ ref('stg_yellow_tripdata') }}
),