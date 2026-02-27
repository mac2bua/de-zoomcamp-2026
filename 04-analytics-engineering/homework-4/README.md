# Module 4 Homework - Analytics Engineering

## Setup Status

### ✅ Completed
- [x] GCP Project created: `analytics-eng-with-bq-and-dbt`
- [x] GCS Bucket created: `dezoomcamp-hw4-2026-mac2bua`
- [x] Data uploaded to GCS (Green, Yellow 2019-2020 + FHV 2019)
- [x] External tables created in BigQuery (green_tripdata, yellow_tripdata, fhv_tripdata)
- [x] dbt Cloud project connected to BigQuery
- [x] dbt build run

### Data Details
- **Project:** analytics-eng-with-bq-and-dbt
- **Dataset:** nytaxi
- **Bucket:** dezoomcamp-hw4-2026-mac2bua

### Files in This Folder
- `load_taxi_data.py` - Script to download/upload taxi data to GCS
- `upload_fhv.py` - Script to upload only FHV data (if needed)

---

## Quiz Answers

| # | Question | Answer |
|---|----------|--------|
| 1 | dbt Lineage and Execution | `int_trips_unioned` only |
| 2 | dbt Tests | dbt will fail the test, returning a non-zero exit code |
| 3 | Count records in fct_monthly_zone_revenue | 1284 |
| 4 | Best performing zone for Green Taxis (2020) | East Harlem North |
| 5 | Green Taxi Trip Counts (October 2019) | 384624 |
| 6 | Build Staging Model for FHV Data | 43244693 |

---

## Solution

### Prerequisites

1. Use the dbt project from the course repository:
   ```bash
   cp -r ~/Repositories/data-engineering-zoomcamp/04-analytics-engineering/taxi_rides_ny/* ~/Repositories/de-zoomcamp-2026/04-analytics-engineering/dbt_project/
   ```

2. Configure GCP project ID in `models/staging/sources.yml`:
   - Replace `please-add-your-gcp-project-id-here` with your GCP_PROJECT_ID (e.g., `data-warehouse-and-big-query`)

3. Run dbt build:
   ```bash
   dbt build --target default
   ```

### Queries

**Q1 - dbt Lineage and Execution:**
Which dbt model(s) will be executed when running `dbt build --select int_trips_unioned`?
- Answer: `int_trips_unioned` only

**Q2 - dbt Tests:**
What will happen when running `dbt build --select stg_strip_unioned`?
- Answer: dbt will fail the test, returning a non-zero exit code

**Q3 - Count records:**
```sql
SELECT count(*) FROM `project.nytaxi.fct_monthly_zone_revenue`
```
- Answer: 1284

**Q4 - Best performing zone (Green Taxis 2020):**
```sql
SELECT zone, SUM(total_amount) as total_revenue
FROM `project.nytaxi.fct_monthly_zone_revenue`
WHERE EXTRACT(YEAR FROM pickup_datetime) = 2020
  AND service_type = 'Green'
GROUP BY zone
ORDER BY total_revenue DESC
LIMIT 1
```
- Answer: East Harlem North

**Q5 - Green Taxi Trip Counts (October 2019):**
```sql
SELECT count(*) FROM `project.nytaxi.fct_monthly_zone_revenue`
WHERE EXTRACT(YEAR FROM pickup_datetime) = 2019
  AND EXTRACT(MONTH FROM pickup_datetime) = 10
  AND service_type = 'Green'
```
- Answer: 384624

**Q6 - Build Staging Model for FHV Data:**
- Modify `models/staging/sources.yml` to add the FHV data source
- Run the appropriate query to count FHV records
- Answer: 43244693

---

## Setup Instructions

### 1. Load Data to GCS
```bash
cd homework-4
python load_taxi_data.py
```

### 2. Create External Tables in BigQuery
```sql
-- Green Taxi
CREATE OR REPLACE EXTERNAL TABLE `project.nytaxi.green_tripdata`
OPTIONS (
  format = 'CSV',
  field_delimiter = ',',
  skip_leading_rows = 1,
  uris = ['gs://bucket/green_tripdata_2019-*.csv.gz', 'gs://bucket/green_tripdata_2020-*.csv.gz']
);

-- Yellow Taxi
CREATE OR REPLACE EXTERNAL TABLE `project.nytaxi.yellow_tripdata`
OPTIONS (
  format = 'CSV',
  field_delimiter = ',',
  skip_leading_rows = 1,
  uris = ['gs://bucket/yellow_tripdata_2019-*.csv.gz', 'gs://bucket/yellow_tripdata_2020-*.csv.gz']
);

-- FHV
CREATE OR REPLACE EXTERNAL TABLE `project.nytaxi.fhv_tripdata`
OPTIONS (
  format = 'CSV',
  field_delimiter = ',',
  skip_leading_rows = 1,
  uris = ['gs://bucket/fhv_tripdata_2019-*.csv.gz']
);
```

### 3. Connect dbt Cloud to BigQuery
1. Go to https://cloud.getdbt.com/
2. Create a new project (or use existing)
3. Connect dbt Cloud to BigQuery:
   - Upload service account JSON from project `analytics-eng-with-bq-and-dbt`
   - Set dataset to: `nytaxi`
4. Initialize dbt project in dbt Cloud

### 4. Run dbt Build
In dbt Cloud, run:
```bash
dbt build --target prod
```

This will create all models in BigQuery.
