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

---

## Quiz Answers

| # | Question | Answer |
|---|----------|--------|
| 1 | Bruin Pipeline Structure | |
| 2 | Materialization Strategies | |
| 3 | Pipeline Variables | |
| 4 | Running with Dependencies | |
| 5 | Quality Checks | |
| 6 | Lineage and Dependencies | |
| 7 | First-Time Run | |

---

## Learning Notes

### Key Concepts Learned

1. **Bruin Project Structure**
   - Required: `.bruin.yml`, `pipeline.yml`, `assets/`
   - `.bruin.yml` stays local (contains secrets)
   - `pipeline.yml` defines schedule, variables, default connections

2. **Materialization Strategies**
   - `append` - add new rows only
   - `replace` - truncate and rebuild
   - `time_interval` - incremental by time column
   - `view` - virtual table

3. **Commands**
   - `bruin validate` - check syntax
   - `bruin run` - execute pipeline
   - `bruin lineage` - show dependency graph
   - `--downstream` - run asset + dependents
   - `--full-refresh` - rebuild from scratch

---

## Files in This Folder
- `homework.md` - Original homework questions
- `README.md` - This progress file
