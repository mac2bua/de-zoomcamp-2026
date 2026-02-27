# NYC Taxi Data Analytics Engineering

dbt (data build tool) project for transforming NYC taxi data in BigQuery.

## Setup

- **Platform:** dbt Cloud (not dbt-core locally)
- **Warehouse:** BigQuery
- **GCP Project:** `analytics-eng-with-bq-and-dbt`
- **Dataset:** `nytaxi`
- **Connection:** Service account with JSON key authentication

## Project Structure

```
dbt_project/
├── models/
│   ├── staging/         # Raw source → cleaned staging tables
│   │   ├── sources.yaml         # Source definitions (BigQuery tables)
│   │   ├── stg_green_tripdata.sql
│   │   └── stg_yellow_tripdata.sql
│   ├── intermediate/   # Business logic layer
│   │   └── int_trips_unioned.sql
│   └── marts/          # Final analytics tables
│       ├── dim_zones.sql
│       ├── dim_payment_types.sql
│       ├── dim_vendors.sql
│       ├── fct_trips.sql
│       └── fct_monthly_zone_revenue.sql
```

## Models

### Staging (`models/staging/`)
- **stg_green_tripdata:** Queries `raw_data.green_tripdata`, casts columns to proper types, filters null vendor IDs
- **stg_yellow_tripdata:** Queries `raw_data.yellow_tripdata`, standardizes schema to match green data

### Intermediate (`models/intermediate/`)
- **int_trips_unioned:** UNION ALL of green and yellow staging tables into a single trips dataset

### Marts (`models/marts/`)
- **dim_zones:** Zone dimension table (joined from seed)
- **dim_payment_types:** Payment type dimension (joined from seed)
- **fct_trips:** Fact table with all trips, enriched with zone names and payment descriptions
- **fct_monthly_zone_revenue:** Aggregated monthly revenue by zone and service type

## Progress

- [x] 4.2.1 - dbt Cloud setup
- [x] 4.2.2 - BigQuery connector setup (service account + JSON key)
- [x] 4.3.1 - Sources and staging models
- [x] 4.3.2 - Intermediate models
- [x] 4.4.1 - Marts introduction
- [x] 4.4.2 - Complete fct_trips model
- [x] 4.4.3 - Complete fct_monthly_zone_revenue model
- [ ] 4.5.1 - Documentation
- [ ] 4.6.1 - Homework

**Up next:** 4.4.2 → 4.6.1

## Running the Project

Since this uses dbt Cloud, models are run via the dbt Cloud IDE or CLI with the cloud profile:

```bash
dbt build --target prod
dbt run --target prod
dbt test
```

## Homework

See `../homework-4/README.md` for homework assignments.
