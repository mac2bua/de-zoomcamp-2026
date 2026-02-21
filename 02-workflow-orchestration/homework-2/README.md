# Module 2 Homework — Backfill 2021 (Green + Yellow Taxi)

This folder contains my solutions for the Data Engineering Zoomcamp Module 2 homework.

## Files Added

- `12_backfill_2021.yaml` — Flow to ingest 2021 taxi data (manual execution)
- `13_backfill_2021_scheduled.yaml` — Scheduled flow for 2021 backfill

Both flows are modified versions of the course flows with:
- `2021` added to the year options
- `purge_files` task commented out to retain downloaded CSVs for inspection

## How to Use

### Manual per-month runs
1. Open Kestra UI → Flows → Execute `zoomcamp:12_backfill_2021`
2. Set inputs: `taxi` (yellow/green), `year=2021`, `month=01..07`
3. Execute for each month

### Backfill
1. Open Kestra UI → Flows → Execute `zoomcamp:13_backfill_2021_scheduled`
2. Use the Backfill feature: time range `2021-01-01` to `2021-07-31`
3. Run separately for `taxi=yellow` and `taxi=green`
4. Set timezone to `America/New_York`

## Quiz Answers

| # | Answer |
|---|--------|
| 1 | 128.3 MiB |
| 2 | green_tripdata_2020-04.csv |
| 3 | 24,648,499 |
| 4 | 1,734,051 |
| 5 | 1,925,152 |
| 6 | Add a `timezone` property set to `America/New_York` in the Schedule trigger configuration |

### Queries used

Q3 - Yellow 2020 total rows:
```sql
SELECT COUNT(*)
FROM public.yellow_tripdata
WHERE filename LIKE 'yellow_tripdata_2020-%.csv';
```

Q4 - Green 2020 total rows:
```sql
SELECT COUNT(*)
FROM public.green_tripdata
WHERE filename LIKE 'green_tripdata_2020-%.csv';
```

Q5 - Yellow March 2021 rows:
```sql
SELECT COUNT(*) FROM public.yellow_tripdata 
WHERE filename = 'yellow_tripdata_2021-03.csv';
```
