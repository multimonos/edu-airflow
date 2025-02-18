from typing import cast, Tuple, List
from airflow.models.taskinstance import TaskInstance
from airflow.operators.python import PythonOperator
from airflow.providers.mysql.hooks.mysql import MySqlHook
from datetime import datetime, timedelta
from airflow import DAG


def get_conn():
    hook: MySqlHook = MySqlHook(mysql_conn_id="devmysql")
    return hook.get_conn()


def show_tables() -> None:
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("show tables;")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    cursor.close()
    conn.close()


def fetch_users() -> None:
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("select * from users limit 10;")
    rows: List[Tuple[int, str]] = cursor.fetchall()

    for row in rows:
        print(row)

    cursor.close()
    conn.close()


def create_log_table() -> None:
    conn = get_conn()
    cursor = conn.cursor()
    sql = """
    CREATE TABLE IF NOT EXISTS `logs` (
        `id` int NOT NULL AUTO_INCREMENT,
        `msg` VARCHAR(255) NOT NULL,
        PRIMARY KEY (`id`)
    );
    """
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()


def fetch_logs() -> None:
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("select * from logs;")
    rows: List[Tuple[int, str]] = cursor.fetchall()

    for row in rows:
        print(row)

    cursor.close()
    conn.close()


def insert_user_actions(ti: TaskInstance, dag: DAG) -> None:
    conn = get_conn()
    cursor = conn.cursor()

    # count before
    cursor.execute("select count(*) from logs;")
    rs = cursor.fetchone()
    count_before = rs[0] if rs else 0
    print(f"count= {count_before}")

    # get users
    cursor.execute("select * from users;")
    users: List[Tuple[int, str]] = cursor.fetchall()

    # insert user actions
    for user in users:
        sql = f"insert into logs (msg) VALUES ('{user[1]} -- did a thing -- dag_id={dag.dag_id} -- run={ti.run_id}');"
        cursor.execute(sql)

    conn.commit()

    # count after
    cursor.execute("select count(*) from logs;")
    rs = cursor.fetchone()
    count_after = rs[0] if rs else 0
    print(f"count= {count_after}")

    cursor.close()
    conn.close()


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
    dag_id="mysql_flow",
    default_args=default_args,
    start_date=datetime(2025, 2, 12),
    schedule_interval="@daily",
) as dag:
    # tasks
    task_fetch_users = PythonOperator(
        task_id="fetch_users", python_callable=fetch_users
    )
    task_show_tables = PythonOperator(
        task_id="show_tables", python_callable=show_tables
    )
    task_create_log_table = PythonOperator(
        task_id="maybe_create_log_table", python_callable=create_log_table
    )
    task_reshow_tables = PythonOperator(
        task_id="reshow_tables", python_callable=show_tables
    )
    task_fetch_logs = PythonOperator(task_id="fetch_logs", python_callable=fetch_logs)
    task_insert_user_actions = PythonOperator(
        task_id="insert_user_actions", python_callable=insert_user_actions
    )

    # dag
    (
        task_fetch_users
        >> task_show_tables
        >> task_create_log_table
        >> task_reshow_tables
        >> task_fetch_logs
        >> task_insert_user_actions
    )
