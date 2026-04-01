# Homework 7 - Streaming

---

## ✅ My Answers

### Question 1: Redpanda Version
**Answer**: `v25.3.9`

**How to reproduce**:
```bash
cd 07-streaming/homework-7/
docker compose up -d
docker exec homework-7-redpanda-1 rpk version
```

---

### Question 2: Time to Send Data
**Answer**: `60 seconds` (actual: 55.28 seconds)

**How to reproduce**:
```bash
cd 07-streaming/homework-7/
uv run python producer.py
# Output: "Took 55.28 seconds"
```

---

### Question 3: Trips with Distance > 5 km
**Answer**: `8506`

**How to reproduce**:
```bash
cd 07-streaming/homework-7/
# Make sure data is in Kafka
uv run python producer.py

# Run consumer to count trips > 5km
uv run python consumer.py
# Output: "Trips with distance > 5: 8506"
```

**Note**: If you get a different number, reset the topic:
```bash
docker exec homework-7-redpanda-1 rpk topic delete green-trips
docker exec homework-7-redpanda-1 rpk topic create green-trips
uv run python producer.py
uv run python consumer.py
```

### Question 4: Top PULocationID (5-min Tumbling Window)
**Answer**: `74`

Create the aggregation table in PostgreSQL:

1. Run pgcli: `uvx --with "psycopg[binary]" pgcli -h localhost -p 5432 -U postgres -d postgres`

2. Paste this:

```
CREATE TABLE processed_events_aggregated (
    window_start TIMESTAMP,
    PULocationID INTEGER,
    num_trips BIGINT,
    total_revenue DOUBLE PRECISION,
    PRIMARY KEY (window_start, PULocationID)
);
```

3. Run producer: `uv run producer.py`

4. Submit the Flink job: 

```
docker compose exec jobmanager ./bin/flink run \
  -py /opt/src/job/q4_tumbling_window_pulocation.py \
  --pyFiles /opt/src -d
```

5. Run this SQL query in `pgcli`:

```
postgres@localhost:postgres> SELECT PULocationID, num_trips
 FROM processed_events_aggregated
 ORDER BY num_trips DESC
 LIMIT 3;
+--------------+-----------+
| pulocationid | num_trips |
|--------------+-----------|
| 74           | 61        |
| 74           | 60        |
| 74           | 58        |
+--------------+-----------+
SELECT 3
Time: 0.014s
```

### Question 5: Longest Session Trips
**Answer**: `81`

This question uses a **session window** with a 5-minute gap. Unlike tumbling windows (fixed time buckets), session windows dynamically group events that occur close together in time. When there's a gap of more than 5 minutes between consecutive trips for the same PULocationID, a new session starts.

**Key insight**: The `SESSION` TVF in Flink requires `PARTITION BY <key>` to create separate sessions per key (PULocationID). Without it, all locations are grouped together into one giant session.

**Steps to reproduce**:

1. Create the session results table in PostgreSQL:
```sql
CREATE TABLE session_results (
    PULocationID INT,
    session_start TIMESTAMP,
    session_end TIMESTAMP,
    num_trips BIGINT,
    PRIMARY KEY (PULocationID, session_start)
);
```

2. (Optional) Clear any existing data and recreate the topic:
```bash
docker exec -it homework-7-postgres-1 psql -U postgres -d postgres -c "TRUNCATE session_results;"
docker exec -it homework-7-redpanda-1 rpk topic delete green-trips
docker exec -it homework-7-redpanda-1 rpk topic create green-trips
```

3. Run the producer (if not already done):
```bash
uv run producer.py
```

4. Submit the Flink job:
```bash
docker compose exec jobmanager ./bin/flink run \
  -py /opt/src/job/q5_session_window_longest_streak.py \
  --pyFiles /opt/src -d
```

5. Query the results:
```sql
SELECT PULocationID, num_trips, session_start, session_end
FROM session_results
ORDER BY num_trips DESC
LIMIT 5;
```

**Result**:
```
+--------------+-----------+---------------------+---------------------+
| pulocationid | num_trips | session_start       | session_end         |
|--------------+-----------+---------------------+---------------------+
| 74           | 81        | 2025-10-08 06:46:14 | 2025-10-08 08:27:40 |
| 74           | 72        | 2025-10-01 06:52:23 | 2025-10-01 08:23:33 |
| 74           | 64        | 2025-10-22 08:34:10 | 2025-10-22 09:39:03 |
| 74           | 64        | 2025-10-21 06:54:16 | 2025-10-21 08:26:03 |
| 74           | 56        | 2025-10-07 06:57:25 | 2025-10-07 08:26:41 |
+--------------+-----------+---------------------+---------------------+
```

**Flink SQL for SESSION window**:
```sql
INSERT INTO session_results
SELECT
    PULocationID,
    window_start AS session_start,
    window_end AS session_end,
    COUNT(*) AS num_trips
FROM TABLE(
    SESSION(TABLE events PARTITION BY PULocationID, DESCRIPTOR(event_timestamp), INTERVAL '5' MINUTE)
)
GROUP BY PULocationID, window_start, window_end;
```

Note: The `PARTITION BY PULocationID` is critical - it ensures each pickup location has its own independent session windows. Without it, Flink creates one global session for all locations combined.

### Question 6: Hour with Highest Tips
**Answer**: _Working on it with Flink in Codespaces_
Let me try with a proper single tool```

## With call:


 this content:

```markdown
### Question 6: Hour with Highest Tips
**Answer**: `2025-10-16 18:00:00` with **$510.86** in tips

Uses a **1-hour tumbling window** to sum `tip_amount` across all locations (not grouped by PULocationID).

**Steps to reproduce**:

1. **Update producer and models** to include `tip_amount`:
   ```python
   # producer.py - add to columns list
   columns = ['PULocationID', 'DOLocationID', 'trip_distance', 'total_amount', 'tip_amount', 'lpep_pickup_datetime']
   
   # models.py - add to dataclass
   tip_amount: float
   ```

2. Create the PostgreSQL table:
   ```sql
   CREATE TABLE tip_results (
       window_start TIMESTAMP,
       window_end TIMESTAMP,
       total_tips DOUBLE PRECISION,
       PRIMARY KEY (window_start)
   );
   ```

3. **Recreate topic and re-produce** (schema changed!):
   ```bash
   docker exec homework-7-redpanda-1 rpk topic delete green-trips
   docker exec homework-7-redpanda-1 rpk topic create green-trips
   uv run producer.py
   ```

4. Submit the Flink job:
   ```bash
   docker compose exec jobmanager ./bin/flink run \
     -py /opt/src/job/q6_tumbling_window_largest_tip.py \
     --pyFiles /opt/src -d
   ```

5. Query the results:
   ```sql
   SELECT window_start, window_end, total_tips
   FROM tip_results
   ORDER BY total_tips DESC
   LIMIT 5;
   ```

**Top 5 hours**:
```
+---------------------+---------------------+--------------------+
| window_start        | window_end          | total_tips         |
|---------------------+---------------------+--------------------|
| 2025-10-16 18:00:00 | 2025-10-16 19:00:00 | 510.86             |
| 2025-10-30 16:00:00 | 2025-10-30 17:00:00 | 507.10             |
| 2025-10-09 18:00:00 | 2025-10-09 19:00:00 | 472.01             |
| 2025-10-10 17:00:00 | 2025-10-10 18:00:00 | 470.08             |
| 2025-10-16 17:00:00 | 2025-10-16 18:00:00 | 445.01             |
+---------------------+---------------------+--------------------+
```

---

## 🔧 Troubleshooting & Learnings

### 1. SESSION Window `PARTITION BY` is Required (Q5)
**Problem**: Without `PARTITION BY`, SESSION creates one global session for all keys combined.

**Symptom**: A session spanning 17+ hours with 401 trips (all locations merged).

**Fix**: Use `SESSION(TABLE events PARTITION BY PULocationID, DESCRIPTOR(event_timestamp), INTERVAL '5' MINUTE)` to create independent sessions per key.

### 2. NULL Values in Aggregation Results (Q6)
**Problem**: Adding a new field to Flink job but not sending it in Kafka.

**Symptom**: Aggregations return NULL for the new field.

**Debug**: Check raw Kafka messages: `rpk topic consume green-trips --num 1`

**Fix Chain**:
1. Update `producer.py` columns list
2. Update `models.py` dataclass and `ride_from_row()`
3. Delete and recreate topic
4. Re-run producer to send updated schema

### 3. Timestamps as Strings in Kafka
**Problem**: Homework asked to send timestamps as strings, not epoch milliseconds.

**Solution**: Use `TO_TIMESTAMP(lpep_pickup_datetime, 'yyyy-MM-dd HH:mm:ss')` in Flink DDL to convert strings to Flink timestamps.

### 4. Flink Window Syntax Reference
| Window Type | Syntax |
|-------------|--------|
| TUMBLE | `TUMBLE(TABLE t, DESCRIPTOR(timecol), INTERVAL '1' HOUR)` |
| SESSION | `SESSION(TABLE t PARTITION BY key, DESCRIPTOR(timecol), INTERVAL '5' MINUTE)` |

SESSION requires: table with optional PARTITION BY, timecol descriptor, gap interval.

---
```

## Also update the Notes section at the bottom:

Replace:
```markdown
## 📝 Notes

- Q1, Q2, Q3 completed locally on M1 Mac
- Q4, Q5, Q6 completed using GitHub Codespaces (I found Flink compatibility issues on Mac)
- Using Green Taxi Trip data from October 2025
- Redpanda v25.3.9 as Kafka-compatible broker
```

With:
```markdown
## 📝 Notes

- Q1-Q3: Python + Kafka (local or Codespaces)
- Q4-Q6: PyFlink (Codespaces recommended - Flink has issues on M1 Mac)
- Data: Green Taxi Trip data from October 2025
- Broker: Redpanda v25.3.9 (Kafka-compatible)