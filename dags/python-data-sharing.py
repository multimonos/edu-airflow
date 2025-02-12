from airflow import DAG
from datetime import datetime, timedelta
from airflow.models.taskinstance import TaskInstance
from airflow.operators.python import PythonOperator


def greet(age: int, ti: TaskInstance) -> None:
    name: str = ti.xcom_pull(task_ids="get_name")
    print(f"hello {name} ... you are {age} years old")


def get_name():
    return "Foobar"


default_args = {
    "owner": "multimonos",
    "retries": 5,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    default_args=default_args,
    dag_id="python_op_data_share_single",
    description="python task with single return value shared via xcom_pull",
    start_date=datetime(2025, 2, 11),
    schedule_interval="@daily",
) as dag:
    task1 = PythonOperator(
        task_id="greet", python_callable=greet, op_kwargs={"age": 49}
    )

    task2 = PythonOperator(task_id="get_name", python_callable=get_name)

    task2 >> task1
