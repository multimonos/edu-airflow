from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from airflow.models.taskinstance import TaskInstance


def greet(ti: TaskInstance) -> None:
    """pull the values we need from xcom"""
    first_name: str = ti.xcom_pull(task_ids="get_name", key="first_name")
    last_name: str = ti.xcom_pull(task_ids="get_name", key="last_name")
    age: int = ti.xcom_pull(task_ids="get_age", key="age")
    print(f"hello {first_name} {last_name} ... you are {age} years old")


def get_name(ti: TaskInstance) -> None:
    """set firstname, lastname via xcom"""
    ti.xcom_push(key="first_name", value="Blind")
    ti.xcom_push(key="last_name", value="Arsmemmy")


def get_age(ti: TaskInstance) -> None:
    """set age in xcom"""
    ti.xcom_push(key="age", value=48)


default_args = {
    "owner": "multimonos",
    "retries": 5,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    default_args=default_args,
    dag_id="python_op_data_share_many_call_many",
    description="python task with multiple value consumption / production",
    start_date=datetime(2025, 2, 11),
    schedule_interval="@daily",
) as dag:
    task1 = PythonOperator(
        task_id="greet", python_callable=greet, op_kwargs={"age": 49}
    )

    task2 = PythonOperator(task_id="get_name", python_callable=get_name)

    task3 = PythonOperator(task_id="get_age", python_callable=get_age)

    [task2, task3] >> task1  # pyright: ignore[reportUnusedExpression]
