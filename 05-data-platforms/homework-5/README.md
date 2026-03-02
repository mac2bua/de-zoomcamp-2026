# Module 5 Homework - Data Platforms with Bruin

## Setup Status

### ✅ Completed
- [x] Bruin CLI installed
- [x] VS Code extension installed
- [x] Default template initialized (`my-first-pipeline`)
- [x] Zoomcamp template in `zoomcamp/` folder
- [x] DuckDB connection configured
- [x] Pipeline assets created

---

## Quiz Answers (ALL COMPLETE)

| # | Question | Answer |
|---|----------|--------|
| 1 | Bruin Pipeline Structure | `.bruin.yml` and `pipeline/` with `pipeline.yml` and `assets/` |
| 2 | Materialization Strategies | `time_interval` |
| 3 | Pipeline Variables | `bruin run --var 'taxi_types=["yellow"]'` |
| 4 | Running with Dependencies | `bruin run ingestion/trips.py --downstream` |
| 5 | Quality Checks | `name: not_null` |
| 6 | Lineage and Dependencies | `bruin lineage` |
| 7 | First-Time Run | `--full-refresh` |

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

### Q6 - Lineage
- `bruin lineage` shows asset dependency graph

### Q7 - First-Time Run
- `--full-refresh` truncates and rebuilds tables from scratch

---

## Submission

Form: https://courses.datatalks.club/de-zoomcamp-2026/homework/hw5
