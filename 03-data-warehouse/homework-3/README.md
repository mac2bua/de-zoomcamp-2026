# Module 3 Homework - Data Warehouse and BigQuery

## Setup Required Before Answering Quizzes

Before answering the quiz questions, you need to:

1. **Create a GCP Project** with BigQuery enabled
2. **Create a GCS Bucket** to store the data
3. **Upload Yellow Taxi data** (Jan-June 2024, parquet files) to GCS
4. **Create External Table** in BigQuery pointing to GCS
5. **Create Materialized Table** in BigQuery (load data from GCS)

### My Setup
- **GCP Project:** data-warehouse-and-big-query
- **GCS Bucket:** dezoomcamp-hw3-2026-mac2bua
- **Dataset:** nytaxi

### Tables Created
- `external_yellow_data` - External table pointing to GCS
- `yellow_tripdata_non_partitioned` - Materialized table (no partition/cluster)
- `yellow_tripdata_partitioned` - Partitioned by DATE(tpep_dropoff_datetime), clustered by VendorID

### Data Source
- **URL:** https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
- **Data:** Yellow Taxi Trip Records (Parquet) for Jan-June 2024

---

## Quiz Answers

| # | Question | Answer | Method |
|---|----------|--------|--------|
| 1 | Count of records for 2024 Yellow Taxi Data | **20,332,093** | `SELECT COUNT(*) FROM external_yellow_data` |
| 2 | Count distinct PULocationIDs - estimated data read (External vs Materialized) | **0 MB (External) / 155.12 MB (Materialized)** | Hover over the query in BQ to see bytes scanned |
| 3 | Why are estimated bytes different when selecting 1 vs 2 columns? | **Option 1: BigQuery is a columnar database, only scans requested columns** | Run queries: SELECT PULocationID (155 MB) vs SELECT PULocationID, DOLocationID (310 MB) |
| 4 | Records with fare_amount = 0 | **8,333** | `SELECT COUNT(*) WHERE fare_amount = 0` |
| 5 | Best partitioning/clustering strategy (filter by tpep_dropoff_datetime, order by VendorID) | **Partition by tpep_dropoff_datetime and Cluster on VendorID** | Partition for filtering, cluster for ordering |
| 6 | Estimated bytes: non-partitioned vs partitioned (date filter) | **310.24 MB (non-partitioned) / 26.84 MB (partitioned)** | Partition reduces scanned data ~12x |
| 7 | Where is data stored in External Table? | **GCP Bucket** | External tables reference GCS, not BQ storage |
| 8 | Always cluster your data? | **False** | Clustering only beneficial for large tables with frequent filters on clustered columns |
| 9 (Bonus) | SELECT COUNT(*) bytes estimate | **0 bytes** | BigQuery uses table metadata for COUNT(*), no data scan needed |

---

## SQL Queries Used

### Q1 - Count records
```sql
SELECT COUNT(*) FROM `data-warehouse-and-big-query.nytaxi.external_yellow_data`;
```

### Q2 - Distinct PULocationIDs
```sql
-- External Table
SELECT COUNT(DISTINCT PULocationID) 
FROM `data-warehouse-and-big-query.nytaxi.external_yellow_data`;

-- Materialized Table  
SELECT COUNT(DISTINCT PULocationID) 
FROM `data-warehouse-and-big-query.nytaxi.yellow_tripdata_non_partitioned`;
```

### Q3 - Columnar storage
```sql
-- Single column
SELECT PULocationID 
FROM `data-warehouse-and-big-query.nytaxi.yellow_tripdata_non_partitioned`;

-- Two columns
SELECT PULocationID, DOLocationID 
FROM `data-warehouse-and-big-query.nytaxi.yellow_tripdata_non_partitioned`;
```

### Q4 - fare_amount = 0
```sql
SELECT COUNT(*) 
FROM `data-warehouse-and-big-query.nytaxi.external_yellow_data` 
WHERE fare_amount = 0;
```

### Q5 - Create partitioned table
```sql
CREATE OR REPLACE TABLE `data-warehouse-and-big-query.nytaxi.yellow_tripdata_partitioned`
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID
AS SELECT * FROM `data-warehouse-and-big-query.nytaxi.external_yellow_data`;
```

### Q6 - Compare queries
```sql
-- Non-partitioned table
SELECT DISTINCT VendorID 
FROM `data-warehouse-and-big-query.nytaxi.yellow_tripdata_non_partitioned`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';

-- Partitioned table
SELECT DISTINCT VendorID 
FROM `data-warehouse-and-big-query.nytaxi.yellow_tripdata_partitioned`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';
```

### Q9 (Bonus) - COUNT(*)
```sql
SELECT COUNT(*) 
FROM `data-warehouse-and-big-query.nytaxi.yellow_tripdata_non_partitioned`;
```
