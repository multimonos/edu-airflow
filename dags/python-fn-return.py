from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator


def greet(name):
    print(f"hello {name}")


def get_name():
    return "Foobar"


default_args = {
    "owner": "multimonos",
    "retries": 5,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    default_args=default_args,
    dag_id="python_op_returns",
    description="python task with return value",
    start_date=datetime(2025, 2, 11),
    schedule_interval="@daily",
) as dag:
    task1 = PythonOperator(
        task_id="greet", python_callable=greet, op_kwargs={"name": "searaig"}
    )

    task2 = PythonOperator(task_id="get_name", python_callable=get_name)

    task1 >> task2
