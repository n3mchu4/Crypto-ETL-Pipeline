# Crypto ETL Pipeline

> Status:  Complete

## 1. Description

An end-to-end ETL (Extract, Transform, Load) pipeline built to practice
core data engineering skills: scheduled data ingestion, orchestration,
transformation, and data quality testing.

The pipeline automatically fetches daily crypto price data from the
public CoinGecko API, stores the raw JSON, loads it into a DuckDB
warehouse, transforms it into clean, analysis-ready tables using dbt,
and runs the entire flow on an automated daily schedule via Apache
Airflow. Data quality is enforced with dbt tests to catch issues like
nulls or duplicates before they reach the final tables.

The goal was to build a realistic, production-style pipeline pattern
(extract → orchestrate → load → transform → test) using tools commonly
found in modern data teams, rather than a one-off script.

## 2. Architecture

```
CoinGecko API
     |
     v
[Extract - Python] --> raw JSON (data/raw/)
     |
     v
[Airflow DAG] --> orchestrates the daily schedule
     |
     v
[Load raw --> DuckDB] --> raw table
     |
     v
[dbt: staging --> marts] --> clean, analysis-ready data
     |
     v
[dbt test] --> data quality checks (not_null, unique)
```

Both the extract task and the dbt run/test step are chained together
as a single Airflow DAG, triggered manually or on a daily schedule.

## 3. Tech Stack

| Component | Technology |
|---|---|
| Language | Python, SQL |
| Orchestration | Apache Airflow 3.1 |
| Transformation | dbt |
| Data warehouse | DuckDB |
| Packaging | Docker, docker-compose |
| Data source | CoinGecko API |

## 4. Project Structure

```
crypto-etl-pipeline/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── extract/
│   ├── coingecko_client.py     # API calls with retry logic
│   ├── run_extract.py          # entry point, saves timestamped JSON
│   └── load_to_duckdb.py       # loads raw JSON into DuckDB
├── dags/
│   └── crypto_extract_dag.py   # Airflow DAG: extract --> dbt run --> dbt test
├── dbt_project/
│   ├── dbt_project.yml
│   ├── profiles.yml
│   └── models/
│       ├── staging/
│       │   ├── stg_crypto_prices.sql
│       │   └── schema.yml
│       └── marts/
│           ├── mart_crypto_daily.sql
│           └── schema.yml
├── data/
│   ├── raw/                    # extracted JSON files (gitignored)
│   └── warehouse/              # crypto.duckdb (gitignored)
└── logs/                       # Airflow logs (gitignored)
```

## 5. How to Run

```bash
# 1. Initialize the Airflow metadata database (first time only)
docker compose up airflow-init

# 2. Start all services (Postgres, Airflow webserver/scheduler/dag-processor)
docker compose up -d

# 3. Open the Airflow UI
# http://localhost:8081 (or whichever host port is mapped)

# 4. Trigger the DAG manually from the UI, or wait for the daily schedule
```

The DAG runs two chained tasks: `extract_crypto_data` (fetches and
saves raw prices) followed by a dbt task that runs `dbt run` and
`dbt test` against the DuckDB warehouse.

## 6. Results / Demo

A successful run produces:
- A new timestamped JSON file in `data/raw/`
- An updated `crypto.duckdb` warehouse with populated staging and mart tables
- All dbt tests passing (no nulls or duplicates in key columns)

## 7. Lessons Learned

- **Airflow 3.x splits execution across separate processes** (scheduler,
  API server, dag-processor) that communicate over HTTP instead of
  running code directly. Tasks failed instantly with empty logs until
  the scheduler was given the correct `EXECUTION_API_SERVER_URL` to
  reach the webserver.
- **All Airflow services must share the same JWT secret**
  (`AIRFLOW__API_AUTH__JWT_SECRET`). Without it, each container
  generates its own signing key, and inter-service requests fail with
  `Invalid auth token: Signature verification failed` — a failure mode
  that produces no useful task-level log, since it happens before the
  task itself starts.
- **Airflow 3.x removed `airflow users create`** in favor of the Simple
  Auth Manager, configured declaratively via
  `AIRFLOW__CORE__SIMPLE_AUTH_MANAGER_USERS` instead of a CLI command.
- **Debugging "instant failure, no logs" tasks** is best done by
  reading the scheduler's own logs (not the task log) and by manually
  running the same Python entry point inside the container to isolate
  whether the issue is code-level or infrastructure-level.
- Separating retry logic into two layers — short retries inside the
  extract function for transient API errors, and Airflow's own task
  `retries` for full-task failures — made the pipeline resilient
  without over-complicating either layer.