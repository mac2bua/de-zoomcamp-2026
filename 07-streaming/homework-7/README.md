# Homework 7 - Streaming

**Student**: Cristian Martinez  
**Course**: Data Engineering Zoomcamp 2026  
**Status**: In Progress (Q1-Q3 Complete, Q4-Q6 Pending)

---

## ✅ My Answers

### Question 1: Redpanda Version
**Answer**: `v25.3.9`

**How to reproduce**:
```bash
cd 07-streaming/workshop/
docker compose up -d
docker exec workshop-redpanda-1 rpk version
```

---

### Question 2: Time to Send Data
**Answer**: `60 seconds` (actual: 55.28 seconds)

**How to reproduce**:
```bash
cd 07-streaming/workshop/
uv run producer.py
# Output: "Took 55.28 seconds"
```

---

### Question 3: Trips with Distance > 5 km
**Answer**: `8506`

**How to reproduce**:
```bash
cd 07-streaming/workshop/
# Make sure data is in Kafka
uv run producer.py

# Run consumer to count trips > 5km
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

---

## ⏳ Pending Questions

### Question 4: Top PULocationID (5-min Tumbling Window)
**Answer**: _Working on it with Flink in Codespaces_

### Question 5: Longest Session Trips
**Answer**: _Working on it with Flink in Codespaces_

### Question 6: Hour with Highest Tips
**Answer**: _Working on it with Flink in Codespaces_

---

## 🚀 Setup Instructions

### Option 1: GitHub Codespaces (Recommended)

1. Go to your repo: https://github.com/heycris/de-zoomcamp-2026
2. Click **"Code"** → **"Codespaces"** tab
3. Click **"Create codespace on main"**
4. Wait for environment to initialize
5. Follow the commands above

### Option 2: Local (M1 Mac)

```bash
cd 07-streaming/workshop/

# Start services
docker compose up -d

# Install dependencies
uv sync

# Run producer/consumer
uv run producer.py
uv run consumer.py
```

---

## 📁 Files in This Homework

```
homework-7/
├── README.md           # This file - my answers
└── src/                # My code (if needed)

workshop/
├── docker-compose.yml  # Redpanda + Flink + PostgreSQL
├── producer.py         # My Kafka producer (Q2)
├── consumer.py         # My Kafka consumer (Q3)
└── src/
    └── job/
        └── aggregation_job.py  # Workshop example
```

---

## 📝 Notes

- Q1, Q2, Q3 completed locally on M1 Mac
- Q4, Q5, Q6 will be completed using GitHub Codespaces (Flink compatibility)
- Using Green Taxi Trip data from October 2025
- Redpanda v25.3.9 as Kafka-compatible broker

---

## 🔗 Resources

- Course Repo: https://github.com/DataTalksClub/data-engineering-zoomcamp
- Workshop: https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/07-streaming/workshop
- Submission: https://courses.datatalks.club/de-zoomcamp-2026/homework/hw7
