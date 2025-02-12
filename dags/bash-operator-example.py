from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "multimonos",
    "retries": 5,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="bash_op",
    default_args=default_args,
    description="bash tasks example",
    start_date=datetime(2025, 2, 11, 9),
    schedule_interval="@daily",
) as dag:
    task1 = BashOperator(task_id="first_task", bash_command='echo "hello world"')
    task2 = BashOperator(task_id="second_task", bash_command='echo "i am second task"')
    task3 = BashOperator(
        task_id="third_task", bash_command='echo "i am parallel to task 2"'
    )

    task1 >> task2
    task1 >> task3

    # alternative
    # task1 >> [task2,task3]
