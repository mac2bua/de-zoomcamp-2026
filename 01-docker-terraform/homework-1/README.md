# Module 1 Homework: Docker & SQL

## Question 1. Understanding Docker images

Commands: 
* `docker run -it --rm python:3.13 bash`
* `pip --version`

**Answer**: `25.3`

## Question 2. Understanding Docker networking and docker-compose

- Containers running with docker compose run in the same network (homework-1_default in this case) and should talk to each other on internal ports. The host should use external port (5433 for postgres).
- To connect to postgres pgadmin can use the service name (db) or the container name (postgres).

**Answer** (multiple choice):
* db:5432 
* (also valid) postgres:5432


## Question 3. Counting short trips

Query:
```
    SELECT
        COUNT(*) AS short_trips_november_2025
    FROM green_taxi_data
    WHERE trip_distance <= 1
        AND lpep_pickup_datetime >= '2025-11-01'
        AND lpep_pickup_datetime < '2025-12-01'
```

**Answer**:
* 8007

## Question 4. Longest trip for each day

Query:
```
WITH valid_trips AS (
    SELECT
        lpep_pickup_datetime,
        trip_distance
    FROM green_taxi_data
    WHERE trip_distance < 100
        AND lpep_pickup_datetime >= '2025-11-01'
        AND lpep_pickup_datetime < '2025-12-01'
)

SELECT
    DATE(lpep_pickup_datetime) AS pickup_date
FROM valid_trips
ORDER BY trip_distance DESC
LIMIT 1;
```

**Answer**:
* 2025-11-14

## Question 5. Biggest pickup zone

Query:
```
WITH total_amount_per_zone AS (
    SELECT
        z."Zone" as zone,
        z."LocationID" as location_id,
        SUM(t.total_amount) AS total_amount
    FROM green_taxi_data t JOIN taxi_zone_lookup z
        ON t."PULocationID" = z."LocationID"
    WHERE t.trip_distance < 100
        AND DATE(t.lpep_pickup_datetime) = '2025-11-18'
    GROUP BY 1, 2
)

SELECT
    *
FROM total_amount_per_zone
ORDER BY total_amount DESC
LIMIT 1;
```

**Answer**:
* East Harlem North	

# Question 6. Largest tip

Query:
```
WITH tips_and_zones AS (
    SELECT
        pu_zone."Zone" as pickup_zone,
        do_zone."Zone" as dropoff_zone,
        t.tip_amount
    FROM green_taxi_data t JOIN taxi_zone_lookup pu_zone 
        ON t."PULocationID" = pu_zone."LocationID"
        JOIN taxi_zone_lookup do_zone
        ON t."DOLocationID" = do_zone."LocationID"
    WHERE t.trip_distance < 100
        AND t.lpep_pickup_datetime >= '2025-11-01'
        AND t.lpep_pickup_datetime < '2025-12-01'
        AND pu_zone."Zone" = 'East Harlem North'
)

SELECT
    dropoff_zone AS largest_tip_zone
FROM tips_and_zones
ORDER BY tip_amount DESC
LIMIT 1;
```

**Answer**:
* Yorkville West

# 7. Terraform Workflow

## Command: `terraform init`
```
$ terraform init --help

Usage: terraform [global options] init [options]

  Initialize a new or existing Terraform working directory by creating
  initial files, loading any remote state, downloading modules, etc.

  This is the first command that should be run for any new or existing
  Terraform configuration per machine. This sets up all the local data
  necessary to run Terraform that is typically not committed to version
  control.

  This command is always safe to run multiple times. Though subsequent runs
  may give errors, this command will never delete your configuration or
  state. Even so, if you have important information, please back it up prior
  to running this command, just in case.

  ...
  ```


## Command: `terraform apply`
```
$ terraform apply --help

Usage: terraform [global options] apply [options] [PLAN]

  Creates or updates infrastructure according to Terraform configuration
  files in the current directory.

  By default, Terraform will generate a new plan and present it for your
  approval before taking any action. You can optionally provide a plan
  file created by a previous call to "terraform plan", in which case
  Terraform will take the actions described in that plan without any
  confirmation prompt.

Options:

  -auto-approve          Skip interactive approval of plan before applying.

...
```


## Command: `terraform destroy`
```
$ terraform destroy --help

Usage: terraform [global options] destroy [options]

  Destroy Terraform-managed infrastructure.

  This command is a convenience alias for:
      terraform apply -destroy

  This command also accepts many of the plan-customization options accepted by
  the terraform plan command. For more information on those options, run:
      terraform plan -help
...
```

**Answer**:
* `terraform init`, `terraform apply -auto-approve`, `terraform destroy`
