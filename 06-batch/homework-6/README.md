# Module 6: Batch Processing with Apache Spark

This folder contains my solutions for the Data Engineering Zoomcamp Module 6 homework on Batch Processing with Apache Spark.

## Overview

Module 6 covers batch processing fundamentals using Apache Spark:
- Spark installation and setup
- SparkSession and DataFrame API
- Spark SQL for querying data
- Partitioning and data optimization
- Spark UI for monitoring
- RDDs (Resilient Distributed Datasets)

## Setup

### Installation Notes

For this module, I installed PySpark using `uv`:

```bash
uv init --python3.13
uv add pyspark
```

I have also installed Java's OpenJDK@17, which is required for Spark to run.

```bash
brew install openjdk@17
```

And added it to my `PATH`.

**Note:** Unlike older tutorials, you don't need to manually install Spark separately or add it to your PATH. PySpark includes the necessary Spark binaries, so you can start using it directly after installation.

### Running Spark

Spark runs locally in standalone mode for this homework:

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .master("local[*]") \
    .appName('homework-6') \
    .getOrCreate()
```

## Homework Solutions

All homework solutions are in the [`notebooks/homework-6.ipynb`](notebooks/homework-6.ipynb) notebook.

### Question 1: Install Spark and PySpark
- **Answer:** Spark 4.1.1

### Question 2: Yellow November 2025
- Repartitioned data to 4 partitions
- **Answer:** ~24MB per parquet file

### Question 3: Count records
- Trips on November 15th, 2025
- **Answer:** 162,604

### Question 4: Longest trip
- **Answer:** ~90.6 hours

### Question 5: User Interface
- **Answer:** Port 4040

### Question 6: Least frequent pickup location zone
- **Answer:** Arden Heights / Governor's Island / Eltingville (all with 1 trip each)

## Key Learnings

1. **PySpark is self-contained** - No need to manually install Spark or configure PATH variables. The `pyspark` package includes everything needed.

2. **Lazy evaluation** - Spark transformations are lazy; actions like `count()` or `show()` trigger actual computation.

3. **Partitioning matters** - Repartitioning data before writing to parquet creates multiple files that can be processed in parallel.

4. **Spark UI is invaluable** - Running on port 4040, it provides insights into jobs, stages, tasks, and executor metrics.

5. **SQL and DataFrame APIs are interchangeable** - You can register DataFrames as temporary views and run SQL queries, or use the DataFrame API. Both are valid approaches.

## Files

- `notebooks/homework-6.ipynb` - Complete homework solutions
- `pyproject.toml` - Project dependencies (pyspark)
- `test_spark.py` - Basic Spark test script

## Running the Notebook

```bash
# Navigate to the module folder
cd 06-batch

# Run Jupyter notebook
jupyter notebook
```

Or with VS Code:
```bash
# Open the notebook and select the .venv kernel
```

## Resources

- [Module 6 Official README](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/06-batch)
- [2026 Homework Instructions](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/cohorts/2026/06-batch/homework.md)
- [PySpark Documentation](https://spark.apache.org/docs/latest/api/python/)
- [Spark SQL Programming Guide](https://spark.apache.org/docs/latest/sql-programming-guide.html)
