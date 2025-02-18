from datetime import timedelta, datetime
from airflow import DAG
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor

default_args = {
    "owner": "multimonos",
    "retries": 5,
    "retry_delay": timedelta(minutes=10),
}

with DAG(
    dag_id="minio_aws_sensor",
    default_args=default_args,
    start_date=datetime(2025, 2, 17),
    schedule_interval="@daily",
) as dag:
    task1 = S3KeySensor(
        task_id="sense",
        bucket_name="airflow-dev",
        bucket_key="data.csv",
        aws_conn_id="devminio",
    )
