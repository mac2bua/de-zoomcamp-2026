# Module 5 Homework - Data Platforms with Bruin

## Setup Status

### ✅ Completed
- [x] Bruin CLI installed
- [x] VS Code extension installed
- [x] Default template initialized (`my-first-pipeline`)
- [x] Zoomcamp template in `zoomcamp/` folder
- [x] DuckDB connection configured
- [x] Pipeline assets created (trips.py, staging trips.sql, reports trips.sql)

---

## Quiz Answers

| # | Question | Answer |
|---|----------|--------|
| 1 | Bruin Pipeline Structure | `.bruin.yml` and `pipeline/` with `pipeline.yml` and `assets/` |
| 2 | Materialization Strategies | `time_interval` |
| 3 | Pipeline Variables | `bruin run --var 'taxi_types=["yellow"]'` |
| 4 | Running with Dependencies | `bruin run ingestion/trips.py --downstream` |
| 5 | Quality Checks | `name: not_null` |
| 6 | Lineage and Dependencies | `bruin graph` |
| 7 | First-Time Run | |

---

## Learning Notes

### Q1 - Bruin Project Structure
- Required: `.bruin.yml` in root, `pipeline.yml` in `pipeline/`, `assets/` next to `pipeline.yml`

### Q2 - Materialization Strategies
- `time_interval` - delete and re-insert for a time window

### Q3 - Pipeline Variables
- Use `--var` flag with JSON syntax for arrays

### Q4 - Running with Dependencies
- Use `--downstream` flag to run asset + dependents

### Q5 - Quality Checks
- `not_null` check ensures a column has no NULL values

### Q6 - Lineage and Dependencies
- `bruin graph` shows the dependency visualization

---

## Files in This Folder
- `homework.md` - Original homework questions
- `README.md` - This progress file
