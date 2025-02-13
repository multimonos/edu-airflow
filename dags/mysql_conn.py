from airflow.operators.python import PythonOperator
from airflow.providers.mysql.hooks.mysql import MySqlHook
from datetime import datetime, timedelta
from airflow import DAG


def fetch_data() -> None:
    hook: MySqlHook = MySqlHook(mysql_conn_id="devmysql")
    conn = hook.get_conn()
    cursor = conn.cursor()
    cursor.execute("select * from test limit 10;")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    cursor.close()
    conn.close()


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
