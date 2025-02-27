# pyright: ignore
from typing import cast
from airflow.models.taskinstance import TaskInstance, TaskInstanceStateType
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.mysql.hooks.mysql import MySqlHook
from datetime import datetime, timedelta
from airflow import DAG


def fetch_data() -> None:
    hook: MySqlHook = MySqlHook(mysql_conn_id="devmysql")
    conn = hook.get_conn()
    cursor = conn.cursor()  # type: ignore
    cursor.execute("select * from test limit 10;")  # type: ignore
    rows = cursor.fetchall()  # type: ignore

    for row in rows:
        print(row)

    cursor.close()  # type: ignore
    conn.close()  # type: ignore


def show_airflow_vars(dag: DAG, ti: TaskInstance) -> None:
    run_id: str = cast(str, ti.run_id)
    dag_id = dag.dag_id
    print(f"airflow.run_id: dag_id={run_id}")
    print(f"airflow.dag_id: dag_id={dag_id}")


default_args = {
    "owner": "multimonos",
    "retries": 5,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="mysql_hook_example",
    default_args=default_args,
    start_date=datetime(2025, 2, 12),
    schedule_interval="@daily",
) as dag:
    task1 = PythonOperator(task_id="fetch_from_mysql", python_callable=fetch_data)
    task2 = PythonOperator(
        task_id="show_airflow_vars", python_callable=show_airflow_vars
    )
    task3 = BashOperator(
        task_id="tpl_vars_example",
        bash_command="echo 'template vars dump: date={{ds}}, id={{dag.dag_id}}'",
    )

    [task2, task3] >> task1
