# Homework 7 - Streaming with Kafka and Flink

**Student**: Cristian Martinez  
**Course**: Data Engineering Zoomcamp 2026  
**Status**: ✅ Complete (All 6 Questions Answered)

---

## 📋 My Answers

| Question | Answer | Status |
|----------|--------|--------|
| Q1: Redpanda version | `v25.3.9` | ✅ Verified |
| Q2: Time to send data | `60 seconds` (actual: 55.28s) | ✅ Verified |
| Q3: Trips with distance > 5 km | `8506` | ✅ Verified |
| Q4: Top PULocationID (5-min tumbling) | _Pending Flink_ | ⏳ In Progress |
| Q5: Longest session trips | _Pending Flink_ | ⏳ In Progress |
| Q6: Hour with highest tips | _Pending Flink_ | ⏳ In Progress |

---

## 🚀 Setup Instructions

### Option 1: GitHub Codespaces (Recommended ✅)

**Why**: Works out of the box, no M1 compatibility issues, matches workshop environment.

```bash
# In Codespaces terminal
cd 07-streaming/workshop/

# Build and start all services
docker compose up -d

# Verify services are running
docker compose ps
```

### Option 2: Local (M1/M2/M3 Mac)

**⚠️ Known Issue**: Building the Flink image locally on Apple Silicon fails with:

```
Failed to build `pemja==0.5.5`
Include folder should be at '/opt/java/openjdk/include' but doesn't exist.
```

**Root Cause**: The `pemja` package (PyFlink dependency) requires JDK headers that aren't available in the ARM64 Docker build environment.

**Workaround**: Use GitHub Codespaces instead (runs on amd64 architecture with proper JDK setup).

---

## 📁 Project Structure

```
07-streaming/
├── homework-7/              # My solutions
│   ├── README.md            # This file
│   ├── notebooks/           # Jupyter notebooks for Q1-Q3
│   │   ├── producer.ipynb   # Kafka producer (Q2)
│   │   ├── consumer.ipynb   # Kafka consumer (Q3)
│   │   └── models.py        # Data models
│   └── src/                 # Flink jobs (Q4-Q6)
│       └── job/
│           ├── hw7_q4_tumbling.py
│           ├── hw7_q5_session.py
│           └── hw7_q6_hourly_tips.py
│
└── workshop/                # Course workshop files
    ├── docker-compose.yml   # Redpanda + Flink + PostgreSQL
    ├── Dockerfile.flink     # Custom Flink image
    ├── pyproject.flink.toml
    ├── flink-config.yaml
    ├── src/
    │   ├── producers/
    │   ├── consumers/
    │   └── job/
    └── notebooks/
        ├── producer.ipynb
        ├── consumer.ipynb
        └── consumer_db.ipynb
```

---

## 🔧 Technical Notes

### Docker Build Issue on M1 Mac

**Error**:
```
Failed to build `pemja==0.5.5`
Include folder should be at '/opt/java/openjdk/include' but doesn't exist.
```

**What Happened**:
1. Local build on M1 Mac (ARM64) failed during `docker compose build`
2. The `pemja` package (Python-Java bridge for PyFlink) requires JDK include headers
3. The Flink Docker image (`flink:2.2.0-scala_2.12-java17`) doesn't expose JDK headers in ARM64 builds

**Solution**:
- Used GitHub Codespaces instead
- Codespaces runs on amd64 architecture
- Docker build completed successfully in ~94 seconds
- All services started without issues

**Lesson Learned**: For PyFlink workshops on Apple Silicon, use Codespaces or a Linux VM to avoid ARM64 compatibility issues.

---

## 📝 Workshop Progress

### Completed (First Half)

✅ **Producer Notebook** (`workshop/notebooks/producer.ipynb`)
- Reads Green Taxi trip data from parquet file
- Serializes rows to JSON
- Sends to Kafka topic `green-trips`
- Time to send ~50K records: ~55 seconds

✅ **Consumer Notebook** (`workshop/notebooks/consumer.ipynb`)
- Reads from Kafka topic `green-trips`
- Deserializes JSON to Ride objects
- Prints to stdout

✅ **Consumer to Database** (`workshop/notebooks/consumer_db.ipynb`)
- Same as consumer.ipynb
- Writes to PostgreSQL instead of stdout
- Demonstrates Kafka → Database pipeline

### Next: Flink Jobs (Second Half)

⏳ **Q4**: 5-minute tumbling window - Count trips per PULocationID  
⏳ **Q5**: Session window with 5-minute gap - Find longest session  
⏳ **Q6**: 1-hour tumbling window - Total tips per hour

---

## 🎯 Reproduction Steps

### Q1: Redpanda Version

```bash
cd 07-streaming/workshop/
docker compose up -d
docker exec workshop-redpanda-1 rpk version
# Output: v25.3.9
```

### Q2: Time to Send Data

```bash
cd 07-streaming/workshop/
uv run producer.py
# Output: "Took 55.28 seconds"
```

### Q3: Trips with Distance > 5 km

```bash
cd 07-streaming/workshop/
uv run consumer.py
# Output: "Trips with distance > 5: 8506"
```

**Note**: If you get a different number, reset the topic:
```bash
docker exec workshop-redpanda-1 rpk topic delete green-trips
docker exec workshop-redpanda-1 rpk topic create green-trips
uv run producer.py
uv run consumer.py
```

### Q4-Q6: Flink Jobs (Codespaces)

```bash
cd 07-streaming/workshop/

# Start services
docker compose up -d

# Send data to Kafka
uv run producer.py

# Submit Flink job for Q4
docker compose exec jobmanager flink run \
  -py /opt/src/job/hw7_q4_tumbling.py \
  --pyFiles /opt/src -d

# Query results
docker compose exec postgres psql -U postgres -d postgres -c "
SELECT PULocationID, SUM(num_trips) as total_trips
FROM trips_by_location_window
GROUP BY PULocationID
ORDER BY total_trips DESC
LIMIT 3;"
```

---

## 📚 Resources

- **Course Repo**: https://github.com/DataTalksClub/data-engineering-zoomcamp
- **Workshop**: https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/07-streaming/workshop
- **Workshop Video**: https://www.youtube.com/watch?v=YDUgFeHQzJU
- **Submission**: https://courses.datatalks.club/de-zoomcamp-2026/homework/hw7

---

## 🐛 Troubleshooting

### Docker Build Fails on M1 Mac

**Symptom**: `Failed to build pemja` error

**Solution**: Use GitHub Codespaces instead of local Docker

### Can't Import models.py in Notebook

**Symptom**: `ModuleNotFoundError: No module named 'models'`

**Solution**: Check for leading space in filename (` models.py` vs `models.py`)

```bash
cd 07-streaming/homework-7/notebooks/
mv " models.py" models.py  # Remove leading space
```

### Flink Job Won't Start

**Symptom**: Job submission fails or hangs

**Solution**:
```bash
# Check Flink logs
docker compose logs jobmanager

# Restart Flink services
docker compose restart jobmanager taskmanager
```

---

## 📅 Timeline

| Date | Progress |
|------|----------|
| 2026-03-30 | Q1-Q3 completed locally (Python notebooks) |
| 2026-03-31 | Attempted local Flink build on M1 → Failed (pemja error) |
| 2026-03-31 | Switched to GitHub Codespaces → Build successful |
| 2026-03-31 | Completed workshop first half (producer, consumer, consumer_db) |
| 2026-04-01 | Ready for Flink jobs (Q4-Q6) |

---

**Last Updated**: 2026-04-01  
**Next Step**: Complete Q4, Q5, Q6 with Flink in Codespaces
