from datetime import timedelta, datetime
from airflow import DAG
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor

default_args = {
    "owner": "multimonos",
    "retries": 5,
    "retry_delay": timedelta(minutes=10),
}

with DAG(
    dag_id="aws_s3_sensor",
    default_args=default_args,
    start_date=datetime(2025, 2, 17),
    schedule_interval="@daily",
) as dag:
    """
    ## Example,
    - datafile : http://minio:9000/airflow-dev/data.csv
    - timeout: 30 sec
    - poke_internal: 5 sec

    If the expected datafile does not exist then 
    this sensor will run 5 times at seconds=[5,10,15,20,25]
    on the 6th attempt at 30 seconds ( the timeout ) the task
    will FAIL.

    If the data file does not initially exist ... some pokes
    happen and then it is uploaded ( mc cp data/data.csv local/airflow-dev
    then the task will PASS.

    Usefull commands within the `minio-client` container,
    - mc ls local/airflow-dev   
    - mc rm local/airflow-dev/data.csv  
    - mc cp /data/data.csv local/airflow-dev

    ## Test case,

    1) In minio-client,
    docker exec -it minio-client /bin/sh

    mc ls local/airflow-dev \
      && mc rm local/airflow-dev/data.csv \
      && sleep 25 \
      && mc cp /data/data.csv local/airflow-dev \
      && mc ls local/airflow-dev
  
    2) In airflow container,
    airflow dags test minio_aws_sensor

    Expected, 
    - a few "pokes" followed by success in airflow container
    """

    task1 = S3KeySensor(
        task_id="sense",
        bucket_name="airflow-dev",
        bucket_key="data.csv",
        aws_conn_id="devminio",
        mode="poke",  # default mode
        poke_interval=5,  # seconds
        timeout=60,  # seconds
    )
