# Module 4 Homework - Analytics Engineering

## Setup Status

### ✅ Completed
- [x] GCP Project created: `analytics-eng-with-bq-and-dbt`
- [x] GCS Bucket created: `dezoomcamp-hw4-2026-mac2bua`
- [x] Data uploaded to GCS (Green, Yellow 2019-2020 + FHV 2019)
- [x] External tables created in BigQuery (green_tripdata, yellow_tripdata, fhv_tripdata)
- [ ] dbt Cloud project connected to BigQuery
- [ ] dbt build run

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
| 1 | dbt Lineage and Execution | |
| 2 | dbt Tests | |
| 3 | Count records in fct_monthly_zone_revenue | |
| 4 | Best performing zone for Green Taxis (2020) | |
| 5 | Green Taxi Trip Counts (October 2019) | |
| 6 | Build Staging Model for FHV Data | |

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
