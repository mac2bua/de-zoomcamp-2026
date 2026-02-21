# Module 3: Data Warehouse and BigQuery

This folder contains my solutions for Module 3 of the Data Engineering Zoomcamp 2026.

## Topics Covered

- BigQuery basics and SQL
- External tables vs Materialized tables
- Partitioning and Clustering
- Best practices for BigQuery
- Machine Learning in BigQuery

## Homework

See `homework-3/` folder for quiz solutions.

## Quiz Answers

| # | Question | Answer |
|---|----------|--------|
| 1 | Count of records for 2024 Yellow Taxi Data | **20,332,093** ✅ |
| 2 | Count distinct PULocationIDs - estimated data read | **0 MB (External) / 155.12 MB (Materialized)** ✅ |
| 3 | Why are estimated bytes different when selecting 1 vs 2 columns? | **Option 1: Columnar database** ✅ |
| 4 | Records with fare_amount = 0 | **8,333** ✅ |
| 5 | Best partitioning/clustering strategy | **Partition by date, Cluster by VendorID** ✅ |
| 6 | Estimated bytes: non-partitioned vs partitioned | **310.24 MB / 26.84 MB** ✅ |
| 7 | Where is data stored in External Table? | **GCP Bucket** ✅ |
| 8 | Always cluster your data? | **False** ✅ |
| 9 (Bonus) | SELECT COUNT(*) bytes estimate | **0 bytes** ✅ |
