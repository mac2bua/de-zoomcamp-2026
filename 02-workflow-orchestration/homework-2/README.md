# Module 2 Homework — Backfill 2021 (Green + Yellow Taxi)

This folder documents the flows I created to ingest 2021 data and provides the verification steps I used to answer the quiz/homework questions.

## Setting up GCP credentials for the GCP-based flows

To run flows `08_gcp_taxi.yaml` and related GCP pipelines, follow these steps:

### 1. Create a GCP project and service account

- Go to [Google Cloud Console](https://console.cloud.google.com/)
- Create a new project (e.g., `kestra-sandbox-demo`)
- Under **IAM & Admin** → **Service Accounts**, create a new service account (e.g., `will-zoomcamp`)
- Grant the service account the following roles:
  - **BigQuery Admin** — for creating/managing BigQuery datasets and tables
  - **Storage Admin** — for creating/managing GCS buckets
- Create a JSON key for the service account and download it locally

### 2. Create the `.env_encoded` file

Follow [Kestra's Google Credentials Guide](https://kestra.io/docs/how-to-guides/google-credentials):

1. Base64-encode your JSON service account key:
   ```bash
   cat /path/to/your/service-account-key.json | base64
   ```

2. Create a file named `.env_encoded` in the `02-workflow-orchestration` directory with the following content:
   ```
   KESTRA_SECRET_GCP_SERVICE_ACCOUNT=<your-base64-encoded-json>
   ```

3. Place this file in `/Users/cristian/Repositories/de-zoomcamp-2026/02-workflow-orchestration/.env_encoded`

### 3. Update `docker-compose.yaml`

Add the `env_file` directive to the `kestra` service:

```yaml
services:
  kestra:
    env_file: .env_encoded
    image: kestra/kestra:v1.1
    # ... rest of service config
```

### 4. Enable required GCP APIs

In the GCP Console for your project:

- Go to **APIs & Services** → **Enabled APIs & services**
- Search for and enable:
  - **Cloud Storage API**
  - **BigQuery API**

### 5. Create GCP resources using flow `06_gcp_kv.yaml`

First, update `06_gcp_kv.yaml` with your GCP project details:

```yaml
id: 06_gcp_kv
namespace: zoomcamp

tasks:
  - id: gcp_project_id
    type: io.kestra.plugin.core.kv.Set
    key: GCP_PROJECT_ID
    kvType: STRING
    value: your-project-id  # ← Use the PROJECT ID, not the project name

  - id: gcp_location
    type: io.kestra.plugin.core.kv.Set
    key: GCP_LOCATION
    kvType: STRING
    value: europe-west10  # or your preferred region

  - id: gcp_bucket_name
    type: io.kestra.plugin.core.kv.Set
    key: GCP_BUCKET_NAME
    kvType: STRING
    value: kestra-zoomcamp-your-unique-name  # must be globally unique!

  - id: gcp_dataset
    type: io.kestra.plugin.core.kv.Set
    key: GCP_DATASET
    kvType: STRING
    value: zoomcamp

  - id: gcp_creds
    type: io.kestra.plugin.core.kv.Set
    key: GCP_CREDS
    kvType: STRING
    value: "{{secret('GCP_SERVICE_ACCOUNT')}}"
```

### 6. Rebuild and restart Kestra

```bash
cd 02-workflow-orchestration
docker-compose down
docker-compose up -d --build
```

Wait ~30 seconds for Kestra to start.

### 7. Run flow `06_gcp_kv.yaml`

- Open Kestra UI at `http://localhost:8080`
- Navigate to **Flows** → `zoomcamp:06_gcp_kv` and click **Execute**
- This stores your GCP configuration as key-value pairs in Kestra

### 8. Run flow `07_gcp_setup.yaml`

- Navigate to **Flows** → `zoomcamp:07_gcp_setup` and click **Execute**
- This creates the GCS bucket and BigQuery dataset

If you get a `403 Forbidden` error, verify:
- The service account has **Storage Admin** and **BigQuery Admin** roles
- The **Cloud Storage API** and **BigQuery API** are enabled in your GCP project
- You used the **project ID** (not the project name) in `06_gcp_kv.yaml`

### Important: Use Project ID, not Project Name

GCP distinguishes between **project name** and **project ID**. The flows require the **project ID**. You can find this in the GCP Console at the top of the page (it looks like `kestra-sandbox-demo-486815`).

---

Files I added

- `homework-2/12_backfill_2021.yaml`: just a copy of `04_postgres_taxi.yaml` with `2021` added to the `year` select and the `purge_files` task commented out so downloaded CSVs remain available after execution.
- `homework-2/13_backfill_2021_scheduled.yaml` — scheduled flow (same as the scheduled flow in the course) with the `purge_files` task commented out so files remain available for inspection after running/backfilling.


How to use these flows

- Manual per-month runs (flow `12_backfill_2021.yaml`):
   - Open the Kestra UI and run `zoomcamp:12_backfill_2021` manually.
   - For each month of 2021 (01..07) set inputs `taxi` (yellow/green), `year=2021`, `month=01..07` and execute the flow.
   - Because `purge_files` is commented, the downloaded CSV will remain available in the execution outputs so I can inspect the uncompressed file and related metadata from the `extract` task outputs.

- Backfill using the scheduled flow (flow `13_backfill_2021_scheduled.yaml`):
   - Open `zoomcamp:13_backfill_2021_scheduled` in the Kestra UI.
   - Use the UI Backfill feature and set the time range `2021-01-01` → `2021-07-31`.
   - Run the backfill for `taxi=yellow` and then for `taxi=green` (or vice versa).
   - Ensure the schedule timezone is set to `America/New_York` when launching the backfill.

Homework results (final answers)

Below are the concise answers and a one-line method indicating how each was obtained from the execution artifacts.

- Q1: Uncompressed size of `yellow_tripdata_2020-12.csv` — **128.3 MiB**.
   - Method: inspected the `extract` task output file metadata in the Kestra execution outputs (uncompressed bytes reported by the execution storage), converted bytes → MiB.

- Q2: Rendered `file` when `taxi=green`, `year=2020`, `month=04` — **green_tripdata_2020-04.csv**.
   - Method: checked the `file` variable definition and rendered label in the execution.

- Q3: Total rows for Yellow 2020 — **24,648,499**.
   - Method: `SELECT COUNT(*)` group-sum across `public.yellow_tripdata` rows grouped by filenames `yellow_tripdata_2020-%` after ingesting all months.

- Q4: Total rows for Green 2020 — **1,734,051**.
   - Method: `SELECT COUNT(*)` group-sum across `public.green_tripdata` rows grouped by filenames `green_tripdata_2020-%` after ingesting all months.

- Q5: Yellow March 2021 rows — **1,925,152**.
   - Method: `SELECT COUNT(*) FROM public.yellow_tripdata WHERE filename = 'yellow_tripdata_2021-03.csv'` after running the March 2021 ingestion.

- Q6: Configure timezone to New York in Schedule trigger — **Set the `timezone` property to `America/New_York`** in the Schedule trigger configuration.

# My solution

1.  `128.3 MiB`

2. `green_tripdata_2020-04.csv`

3. 

query:
```
SELECT COUNT(*)
FROM public.yellow_tripdata
WHERE filename LIKE 'yellow_tripdata_2020-%.csv';
```

4. 

query:
```
SELECT COUNT(*)
FROM public.green_tripdata
WHERE filename LIKE 'green_tripdata_2020-%.csv';
```
