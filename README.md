# Crypto ETL Pipeline

> Status: 🚧 In progress — Extract + Orchestration (Airflow) complete,
> Transformation (dbt) in progress

## 1. Description

This project is an end-to-end ETL (Extract, Transform, Load) pipeline
built to practice core data engineering skills: scheduled data
ingestion, orchestration, transformation, and data quality testing.

The pipeline automatically fetches daily crypto price data from the
public CoinGecko API, stores the raw data, transforms it into clean,
analysis-ready tables using dbt, and runs on an automated schedule via
Apache Airflow. Data quality is enforced with dbt tests to catch
issues like nulls, duplicates, or unexpected values before they reach
the final tables.

The goal is to demonstrate a realistic, production-style pipeline
pattern (extract → orchestrate → load → transform → test) rather than
a one-off script, using tools commonly found in modern data teams.

_(Once complete: rewrite this to describe what the pipeline actually
does, e.g. "runs daily, tracks prices for 10 coins, aggregates a
weekly price-movement report")_

## 2. Architecture (planned)

```
CoinGecko API
     |
     v
[Extract - Python] --> raw JSON (staging)          ( done )
     |
     v
[Airflow DAG] --> orchestrates the daily schedule   ( done )
     |
     v
[Load raw --> DuckDB]                               ( in progress )
     |
     v
[dbt: staging --> marts] --> clean, analysis-ready  ( in progress )
     |
     v
[dbt test] --> data quality checks                  ( in progress )
```

_(Once fully complete: remove the status markers and replace with the
final architecture if anything changed)_

## 3. Tech Stack

| Component | Technology |
|---|---|
| Language | Python, SQL |
| Orchestration | Apache Airflow |
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
│   ├── coingecko_client.py    # API calls with retry logic
│   └── run_extract.py          # entry point, saves timestamped JSON
├── dags/
│   └── crypto_extract_dag.py   # Airflow DAG definition
├── data/
│   └── raw/                    # extracted JSON files (gitignored)
└── dbt_project/                # in progress
```

## 5. How to Run

```bash
# 1. Initialize the Airflow metadata database (first time only)
docker compose up airflow-init

# 2. Start all services (Postgres, Airflow webserver/scheduler/dag-processor)
docker compose up -d

# 3. Open the Airflow UI
# http://localhost:8081 (or whichever host port is mapped)

# 4. Trigger the DAG manually, or wait for the daily schedule
```

_(Once dbt is added: extend this section with `dbt run` / `dbt test`
instructions)_