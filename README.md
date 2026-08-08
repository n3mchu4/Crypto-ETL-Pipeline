# Crypto-ETL-Pipeline# Crypto ETL Pipeline

> Status: In progress (draft README — update once complete)

## 1. Goal

An automated pipeline that fetches crypto price data from the CoinGecko
API, cleans and transforms it, loads it into a data warehouse, and runs
on a schedule with data quality tests.

_(Once complete: rewrite this briefly to describe what the pipeline
actually does, e.g. "runs daily, tracks prices for 10 coins, aggregates
a weekly price-movement report")_

## 2. Architecture (planned)

```
CoinGecko API
     |
     v
[Extract - Python] --> raw JSON (staging)
     |
     v
[Airflow DAG] --> orchestrates the daily schedule
     |
     v
[Load raw --> DuckDB]
     |
     v
[dbt: staging --> marts] --> clean, analysis-ready data
     |
     v
[dbt test] --> data quality checks
```

_(Once complete: replace with the actual architecture if it changed)_

## 3. Tech Stack

| Component | Technology |
|---|---|
| Language | Python, SQL |
| Orchestration | Apache Airflow |
| Transformation | dbt |
| Data warehouse | DuckDB |
| Packaging | Docker, docker-compose |
| Data source | CoinGecko API |