/*
- Filter out records where dispatching_base_num IS NULL
- Rename fields to match your project's naming conventions (e.g., PUlocationID → pickup_location_id)
*/

WITH source AS (
    SELECT *
    FROM {{ source("raw", "fhv_tripdata") }}
),

renamed AS (
    SELECT 
        dispatching_base_num,
        pickup_datetime,
        dropOff_datetime AS dropoff_datetime,
        PUlocationID AS pickup_location_id,
        DOlocationID AS dropoff_location_id,
        sr_flag AS sr_flag,
        Affiliated_base_number AS affiliated_base_number
    FROM source 
    WHERE dispatching_base_num IS NOT NULL
)

SELECT *
FROM renamed