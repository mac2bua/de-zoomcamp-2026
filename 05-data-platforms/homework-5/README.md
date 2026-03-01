# Module 5 Homework - Data Platforms with Bruin

## Setup Status

### ✅ Completed
- [x] Bruin CLI installed
- [x] VS Code extension installed
- [x] Default template initialized (`my-first-pipeline`)
- [x] Zoomcamp template copied to `zoomcamp/` folder
- [x] DuckDB connection configured

### Practice Commands Run
- `bruin validate .` - Validate pipeline
- `bruin build .` - Build pipeline
- `bruin run .` - Run pipeline
- `bruin lineage .` - View dependencies
- `bruin run . --var 'taxi_types=["yellow"]'` - Override variable

---

## Quiz Answers

| # | Question | Answer |
|---|----------|--------|
| 1 | Bruin Pipeline Structure | `.bruin.yml` and `pipeline/` with `pipeline.yml` and `assets/` |
| 2 | Materialization Strategies | `time_interval` |
| 3 | Pipeline Variables | `bruin run --var 'taxi_types=["yellow"]'` |
| 4 | Running with Dependencies | |
| 5 | Quality Checks | |
| 6 | Lineage and Dependencies | |
| 7 | First-Time Run | |

---

## Learning Notes

### Q1 - Bruin Project Structure
- Required: `.bruin.yml` in root, `pipeline.yml` in `pipeline/`, `assets/` next to `pipeline.yml`
- `.bruin.yml` stays local (contains secrets)
- `pipeline.yml` defines schedule, variables, default connections

### Q2 - Materialization Strategies
- `append` - add new rows only
- `replace` - truncate and rebuild entire table
- `time_interval` - delete and re-insert for a time window
- `view` - virtual table

### Q3 - Pipeline Variables
- Use `--var` flag with JSON syntax
- Array: `'taxi_types=["yellow"]'`
- Tested with: `bruin run . --var 'taxi_types=["yellow"]'`

### Q4 - Running with Dependencies
- Use `--downstream` flag to run asset + all dependents

---

## Files in This Folder
- `homework.md` - Original homework questions
- `README.md` - This progress file
