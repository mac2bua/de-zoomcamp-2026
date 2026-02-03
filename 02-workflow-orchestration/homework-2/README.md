# Module 2 Homework — Backfill 2021 (Green + Yellow Taxi)

This folder contains the files I added to extend the course flows for the Module 2 homework.

What I changed

- Updated `flows/04_postgres_taxi.yaml` to include `2021` in the `year` input values and added a sample schedule trigger with `timezone: "America/New_York"`.
- Added a helper flow `flows/05_backfill_2021.yaml` that demonstrates how to generate the 2021 (taxi, year, month) combinations and trigger executions for `04_postgres_taxi` using the Kestra API.
- Added a small verification script `scripts/verify_counts_2021.py` to download the files for 2021 months and print the line counts (useful to validate ingestion results locally before/after running the flows).

How to use

1. Backfill using the Kestra UI (recommended)
   - Open the Kestra UI and navigate to the `zoomcamp:04_postgres_taxi` flow.
   - Use the **Backfill / Schedule** functionality and set the time range `2021-01-01` → `2021-07-31`.
   - Select the `taxi` input (yellow or green) and run the backfill for each taxi type (or do two backfills).
   - Make sure to set the schedule timezone to `America/New_York` when configuring the backfill.

2. Trigger via helper flow (script that posts to Kestra API)
   - Deploy Kestra and ensure the API is reachable (e.g. `http://localhost:8080`).
   - Run the helper flow `zoomcamp:05_backfill_2021` in the UI with `kestra_host` and optional `kestra_api_key` (or run the flow directly).
   - The helper flow will POST to the Kestra API endpoint `/api/v1/executions` to start executions of `zoomcamp:04_postgres_taxi` for all months 01..07 and both taxi types.
   - Note: you may need to adapt the API endpoint or authorization header depending on your Kestra installation.

3. Verify counts locally (optional)
   - Run the verification script to download the 2021 monthly CSVs from the DataTalksClub release and count rows:

     ```bash
     python02-workflow-orchestration/scripts/verify_counts_2021.py
     ```

Notes & challenge

- The ForEach + Subflow challenge can be implemented with a dedicated `ForEach` task that iterates over the generated list and calls the `04_postgres_taxi` flow as a Subflow task. If you prefer doing it that way, I included a helper flow that demonstrates triggering via the Kestra API instead (more portable and doesn't depend on exact in-cluster Subflow plugin names).

Files added/changed

- modified: `flows/04_postgres_taxi.yaml` (added 2021 year selection + schedule example)
- added: `flows/05_backfill_2021.yaml` (helper flow that posts to Kestra API)
- added: `homework-2/README.md` (this file)
- added: `scripts/verify_counts_2021.py` (download + count verification script)

If you'd like, I can also add a short notebook that visualizes the counts and file sizes. Happy to add that next.