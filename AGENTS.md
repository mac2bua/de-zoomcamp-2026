# AGENTS.md

This file provides guidance to agents (i.e., ADAL) when working with code in this repository.

## Repository Overview

**Data Engineering Zoomcamp 2026** - Course materials and exercises for learning data engineering with Docker, Terraform, and data pipelines.

- **Structure**: Organized by course modules (01-docker-terraform, etc.)
- **Environment**: GitHub Codespaces/devcontainer with Ubuntu + Terraform
- **Language**: Python 3.13+
- **Package Manager**: `uv` (modern Python package manager - NOT pip/poetry)

## Essential Commands

### Package Management with uv

**CRITICAL**: This project uses `uv`, not pip or poetry. All Python dependencies are managed through `uv`.

```bash
# Install dependencies (from uv.lock)
cd 01-docker-terraform/docker-workshop
uv sync

# Run Python scripts
uv run python main.py
uv run python ingest_data.py --help

# Add new dependencies
uv add <package-name>

# Run Jupyter notebook
uv run jupyter notebook
```

### Docker Services

**Local PostgreSQL + pgAdmin setup** for data engineering exercises:

```bash
cd 01-docker-terraform/docker-workshop

# Start all services (Postgres + pgAdmin)
docker compose up -d

# Stop services
docker compose down

# View logs
docker compose logs -f
docker compose logs db        # Postgres only
docker compose logs pgadmin   # pgAdmin only

# Rebuild after changes
docker compose up -d --build
```

**Service Access**:
- PostgreSQL: `localhost:5433` (external) - **NOTE: Non-standard port!**
- pgAdmin: `http://localhost:8080`
  - Login: `pgadmin@pgadmin.com` / `pgadmin`

**IMPORTANT Port Mapping**:
- Postgres uses port **5433** externally (not default 5432) to avoid conflicts
- Within Docker network, containers use internal port 5432
- Connection from host: `localhost:5433`
- Connection between containers: `db:5432` or `postgres:5432`

### Data Ingestion

NYC Taxi dataset ingestion tool with CLI options:

```bash
cd 01-docker-terraform/docker-workshop

# Basic ingestion (defaults: 2021-01, localhost:5432)
uv run python ingest_data.py

# Custom parameters
uv run python ingest_data.py \
  --year 2021 \
  --month 1 \
  --pg-host localhost \
  --pg-port 5433 \
  --pg-user postgres \
  --pg-pass postgres \
  --pg-db ny_taxi \
  --target-table yellow_taxi_data \
  --chunksize 100000

# Connect to containerized Postgres from host
uv run python ingest_data.py --pg-port 5433 --pg-user postgres --pg-pass postgres

# View all options
uv run python ingest_data.py --help
```

**Data Source**: NYC taxi data from `https://github.com/DataTalksClub/nyc-tlc-data/releases`

### Database Access

**From host machine**:
```bash
# Using pgcli (installed as dev dependency)
cd 01-docker-terraform/docker-workshop
uv run pgcli -h localhost -p 5433 -U postgres -d ny_taxi

# Password: postgres
```

**From pgAdmin** (http://localhost:8080):
1. Add Server: `db` or `postgres` as hostname
2. Port: `5432` (internal Docker network port)
3. Username: `postgres`, Password: `postgres`
4. Database: `ny_taxi`

### Terraform

```bash
cd 01-docker-terraform/terraform-demo

# Initialize Terraform
terraform init

# Plan changes
terraform plan

# Apply configuration
terraform apply

# Destroy resources
terraform destroy
```

## Architecture & Data Flow

### Docker Compose Services

**Network Architecture**:
```
Host Machine (localhost)
  ↓ port 5433
[postgres:5433] ← Mapped to → [postgres:5432 in container]
  ↓ port 8080
[pgadmin:8080] ← Mapped to → [pgadmin:80 in container]

Internal Docker Network (homework-1_default):
  - Services communicate via service names
  - db:5432 or postgres:5432 (internal port)
```

**Persistent Volumes**:
- `vol-pgdata`: PostgreSQL data directory
- `vol-pgadmin_data`: pgAdmin configuration

**Services auto-start** on `docker compose up` and share the same network.

### Data Ingestion Flow

**Pipeline**: `ingest_data.py` → Download CSV.gz → Chunk → SQLAlchemy → PostgreSQL

1. **Download**: Fetches NYC taxi data from GitHub releases (compressed CSV)
2. **Chunking**: Reads in configurable chunks (default 100k rows) for memory efficiency
3. **Schema Creation**: First chunk creates table with proper schema (no data)
4. **Batch Insert**: Each chunk appended to table via SQLAlchemy
5. **Progress**: tqdm progress bar for monitoring

**Key Implementation Details**:
- Uses pandas with explicit dtypes for proper type handling
- Parse dates: `tpep_pickup_datetime`, `tpep_dropoff_datetime`
- SQLAlchemy engine: `postgresql://{user}:{pass}@{host}:{port}/{db}`
- Table creation: `if_exists="replace"` for schema, `if_exists="append"` for data

## Key Files & Entry Points

### Main Scripts
- `01-docker-terraform/docker-workshop/main.py` - Simple entry point (hello world)
- `01-docker-terraform/docker-workshop/ingest_data.py` - NYC taxi data ingestion CLI
- `01-docker-terraform/docker-workshop/pipeline.py` - Data pipeline implementation
- `01-docker-terraform/docker-workshop/notebook.ipynb` - Jupyter notebook for exploration

### Configuration
- `01-docker-terraform/docker-workshop/pyproject.toml` - Python dependencies (uv-managed)
- `01-docker-terraform/docker-workshop/docker-compose.yaml` - Local services setup
- `.devcontainer/devcontainer.json` - Codespaces/devcontainer config
- `01-docker-terraform/terraform-demo/main.tf` - Terraform infrastructure

### Dependencies
**Production**:
- `pandas` (3.0.0+) - Data manipulation
- `sqlalchemy` (2.0.46+) - Database ORM
- `psycopg2-binary` - PostgreSQL driver
- `click` - CLI framework
- `pyarrow` - Columnar data format
- `tqdm` - Progress bars

**Development**:
- `jupyter` - Interactive notebooks
- `pgcli` - PostgreSQL CLI client

## Gotchas & Important Notes

### Package Management
- **DO NOT use pip install** - this project uses `uv`
- Always run Python scripts with `uv run python script.py`
- Lock file: `uv.lock` contains exact dependency versions

### Docker & Networking
- **External port is 5433**, not 5432 (check connection strings!)
- From host: use `localhost:5433`
- Between containers: use `db:5432` or `postgres:5432`
- Service names (`db`) work as hostnames within Docker network
- Container names (`postgres`) also work but service names preferred

### Data Ingestion
- Data downloads from GitHub on each run (no local cache)
- Default chunk size (100k) balances memory vs. speed
- First run creates table schema - subsequent runs append
- Use `--pg-port 5433` when connecting from host machine

### Environment
- Python 3.13+ required (project uses latest features)
- Terraform pre-installed in devcontainer
- Git repository on `main` branch

## Module Structure

```
01-docker-terraform/
├── docker-workshop/      # Main workshop: Docker, Python, data ingestion
│   ├── pyproject.toml    # uv dependencies
│   ├── docker-compose.yaml  # Postgres + pgAdmin
│   ├── ingest_data.py    # Data ingestion CLI
│   └── notebook.ipynb    # Jupyter exploration
├── homework-1/           # Homework assignments and solutions
│   └── docker-compose.yaml  # Exercise-specific setup
└── terraform-demo/       # Terraform infrastructure as code
    └── main.tf           # Terraform configuration
```

## Development Workflow

1. **Start Services**: `cd 01-docker-terraform/docker-workshop && docker compose up -d`
2. **Install Dependencies**: `uv sync`
3. **Verify Connection**: `uv run pgcli -h localhost -p 5433 -U postgres -d ny_taxi`
4. **Run Ingestion**: `uv run python ingest_data.py --pg-port 5433 --pg-user postgres --pg-pass postgres`
5. **Explore Data**: Open pgAdmin or use `uv run jupyter notebook`
6. **Stop Services**: `docker compose down`

## Database Credentials

**PostgreSQL** (from docker-compose.yaml):
- User: `postgres`
- Password: `postgres`
- Database: `ny_taxi`
- Port (external): `5433`
- Port (internal): `5432`

**pgAdmin**:
- Email: `pgadmin@pgadmin.com`
- Password: `pgadmin`
