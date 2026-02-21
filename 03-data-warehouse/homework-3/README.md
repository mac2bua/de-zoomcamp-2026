# Module 3 Homework

## Setup Required Before Answering Quizzes

Before answering the quiz questions, you need to:

1. **Create a GCP Project** with BigQuery enabled
2. **Create a GCS Bucket** to store the data
3. **Upload Yellow Taxi data** (Jan-June 2024, parquet files) to GCS
4. **Create External Table** in BigQuery pointing to GCS
5. **Create Materialized Table** in BigQuery (load data from GCS)

### Data Source
- **URL:** https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
- **Data:** Yellow Taxi Trip Records (Parquet) for Jan-June 2024

### Load Script
See `load_yellow_taxi_data.py` in the course repo for uploading data to GCS.

---

## Quiz Questions

### Question 1
What is count of records for the 2024 Yellow Taxi Data?

### Question 2
Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables.
What is the **estimated amount** of data that will be read when this query is executed on the External Table and the Table?

### Question 3
Write a query to retrieve the PULocationID from the table (not the external table) in BigQuery. Now write a query to retrieve the PULocationID and DOLocationID on the same table. Why are the estimated number of Bytes different?

### Question 4
How many records have a fare_amount of 0?

### Question 5
What is the best strategy to make an optimized table in Big Query if your query will always filter based on tpep_dropoff_datetime and order the results by VendorID?

### Question 6
Write a query to retrieve the distinct VendorIDs between tpep_dropoff_datetime 2024-03-01 and 2024-03-15 (inclusive). Compare estimated bytes between non-partitioned and partitioned tables.

### Question 7
Where is the data stored in the External Table you created?

### Question 8
It is best practice in Big Query to always cluster your data?

### Question 9 (Bonus)
Write a `SELECT count(*)` query FROM the materialized table. How many bytes does it estimate will be read? Why?
