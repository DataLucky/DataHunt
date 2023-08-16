import json
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.providers.http.sensors.http import HttpSensor

from dags.scripts.to_s3 import upload_to_s3

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
    is_weather_ready = HttpSensor(
        task_id='is_example_dag_weather_api',
        http_conn_id='weather_api',
        endpoint=".../"
    )

    extract_data = SimpleHttpOperator(
        task_id='extract_example_api',
        http_conn_id='api',
        endpoint="../",
        method='GET',
        response_filter=lambda r: json.load(r.text),
        log_response=True
    )

    load_task = PythonOperator(
        task_id='upload_to_s3',
        python_callable=upload_to_s3,
        dag=dag,
    )
    # error = DummyOperator(task_id='error')

is_weather_ready >> extract_data >> load_task
# [load_task, error]
