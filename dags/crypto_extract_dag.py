from airflow import DAG
from airflow.operators.python import PythonOperator

from extract.run_extract import main

from datetime import datetime


with DAG(
    dag_id="crypto_extract",
    start_date=datetime(2026, 8, 1),
    schedule="@daily",
    catchup=False,
) as dag:

    extract_task = PythonOperator(
        task_id="extract_crypto_data",
        python_callable=main,
    )