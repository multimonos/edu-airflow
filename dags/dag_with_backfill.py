from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta


default_args = {
    "owner": "multimonos",
    "retries": 5,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="backfill_example",
    default_args=default_args,
    start_date=datetime(2025, 2, 1),  # set to date in past
    schedule_interval="@daily",
    catchup=False,  # all missed executions will NOT be run
) as dag:
    # how to backfill?
    # run `shell/path/to/airflow dags backfill -s 2025-02-01 -e 2025-02-12 backfill_example`
    # aka `shell/path/to/airflow dags backfill -s <start-date> -e <end-date> <dag-id>`

    task1 = BashOperator(task_id="task1", bash_command='echo "simple bash cmd yo"')
