from airflow import DAG
from airflow.operators.bash import BashOperator

from datetime import timedelta

from pendulum import datetime


default_args = {
    "owner": "multimonos",
    "retries": 5,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="catchup_and_backfill",
    default_args=default_args,
    start_date=datetime(2025, 2, 1),
    schedule_interval="@daily",
    catchup=True,
) as dag:
    task1 = BashOperator(task_id="task1", bash_command='echo "simple bash cmd yo"')
