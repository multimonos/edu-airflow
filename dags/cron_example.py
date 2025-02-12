from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta


default_args = {
    "owner": "multimonos",
    "retries": 5,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="cron_example",
    default_args=default_args,
    start_date=datetime(2025, 2, 12), 
    schedule_interval="0 3 * * Tue,Fri"
) as dag:
    task1 = BashOperator(task_id="task1", bash_command='echo "i was run with cron"')
