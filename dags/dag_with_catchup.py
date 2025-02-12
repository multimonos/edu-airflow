from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta


default_args = {
    "owner": "multimonos",
    "retries": 5,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="catchup_example",
    default_args=default_args,
    start_date=datetime(2025, 2, 1),  # set to date in past
    schedule_interval="@daily",
    catchup=True,  # all missed executions will be run
) as dag:
    task1 = BashOperator(task_id="task1", bash_command='echo "simple bash cmd yo"')
