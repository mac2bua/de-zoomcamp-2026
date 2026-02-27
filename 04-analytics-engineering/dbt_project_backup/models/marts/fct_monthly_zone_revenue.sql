-- Data mart for monthly revenue analysis by pickup zone and service type
-- This aggregation is optimized for business reporting and dashboards
-- Enables analysis of revenue trends across different zones and taxi types

SELECT
    -- Grouping dimensions
    COALESCE(pickup_zone, 'Unknown Zone') as pickup_zone,
    {% if target.type == 'bigquery' %}
        CAST(DATE_TRUNC(pickup_datetime, MONTH) AS DATE) 
    {% elif target.type == 'duckdb' %}
        DATE_TRUNC('month', pickup_datetime)
    {% endif %} as revenue_month,
    service_type,
    
    -- Revenue breakdown (summed by zone, month, and service type)
    SUM(fare_amount) as revenue_monthly_fare,
    SUM(extra) as revenue_monthly_extra,
    SUM(mta_tax) as revenue_monthly_mta_tax,
    SUM(tip_amount) as revenue_monthly_tip_amount,
    SUM(tolls_amount) as revenue_monthly_tolls_amount,
    SUM(ehail_fee) as revenue_monthly_ehail_fee,
    SUM(improvement_surcharge) as revenue_monthly_improvement_surcharge,
    SUM(total_amount) as revenue_monthly_total_amount,
    
    -- Additional metrics for operational analysis
    COUNT(trip_id) as total_monthly_trips,
    AVG(passenger_count) as avg_monthly_passenger_count,
    AVG(trip_distance) as avg_monthly_trip_distance

FROM {{ ref('fct_trips') }}

GROUP BY pickup_zone, revenue_month, service_type
