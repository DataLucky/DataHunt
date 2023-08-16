import json
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.providers.http.sensors.http import HttpSensor

from scripts.to_s3 import upload_to_s3

BASE_URL = "https://lang-popopy.onrender.com/"

default_params = {
    "owner": 'airflow',
    "depends_on_past": False,
    "start_date": datetime(2023, 8, 15),
    "email": [
        "hei.nalisoa@gmail.com",
        "hei.tsirimaholy@gmail.com"
    ],
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=2)
}

with DAG(dag_id='dag_data_lake',
         default_args=default_params,
         schedule="@hourly",
         catchup=False) as dag:
    is_API_ready = HttpSensor(
        task_id='is_api_ready_to_consumes',
        http_conn_id='lang_popy',
        endpoint=BASE_URL + "/ping"
    )

    extract_data_stackoverflow = SimpleHttpOperator(
        task_id='extract_data_stackoverflow',
        http_conn_id='api',
        endpoint=BASE_URL + "/stackoverflow",
        method='GET',
        response_filter=lambda r: json.load(r.text),
        log_response=True
    )

    extract_data_indeed = SimpleHttpOperator(
        task_id='extract_data_indeed',
        retries=6,
        http_conn_id='api',
        endpoint=BASE_URL + "/indeed",
        method='GET',
        response_filter=lambda r: json.load(r.text),
        log_response=True
    )

    load_task_indeed = PythonOperator(
        task_id='upload_to_s3',
        python_callable=upload_to_s3,
        dag=dag,
    )

is_API_ready >> extract_data_indeed >> load_task_indeed
