from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from extract.run_extract import main


with DAG(
    dag_id="crypto_extract_dag",
    start_date=datetime(2026, 8, 14),
    schedule="@daily",
    catchup=False,
) as dag:

    extract_crypto = PythonOperator(
        task_id="extract_crypto",
        python_callable=main,
    )