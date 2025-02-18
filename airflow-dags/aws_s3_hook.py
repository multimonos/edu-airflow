from datetime import datetime, timedelta
import csv
from airflow.operators.python import PythonOperator
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

postgres_conn_id = "devpostgres"


def show_orders() -> None:
    hook = PostgresHook(postgres_conn_id=postgres_conn_id)
    conn = hook.get_conn()
    cursor = conn.cursor()
    cursor.execute("select * from orders limit 10;")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    cursor.close()
    conn.close()


def write_orders_csv() -> None:
    # get data
    hook = PostgresHook(postgres_conn_id=postgres_conn_id)
    conn = hook.get_conn()
    cursor = conn.cursor()
    cursor.execute("select * from orders limit 10;")

    # write
    ofile = "/home/airflow/dags/orders_.csv"
    with open(ofile, "w+") as fp:
        writer = csv.writer(fp)
        print(f"cursor.description: {cursor.description}")
        writer.writerow([i[0] for i in cursor.description])
        writer.writerows(cursor)
    cursor.close()
    conn.close()


# dag
default_args = {
    "owner": "multimonos",
    "retries": 5,
    "retry_delay": timedelta(minutes=10),
}

with DAG(
    dag_id="aws_s3_hook",
    default_args=default_args,
    start_date=datetime(2025, 2, 17),
    schedule_interval="@daily",
) as dag:
    """
    Preconditions,
    - i manually loaded the postgres-src/orders.csv vi psql using 'copy orders ... from ...' stmt

    This dag does the following,
    - create table in postgres
    - collect order data
    - write order data to file
    - upload file to s3 like bucket
    """
    maybe_create_table = PostgresOperator(
        task_id="maybe_create_table",
        postgres_conn_id=postgres_conn_id,
        sql="""
        create table if not exists orders (
            order_id character varying,
            date date,
            product_name character varying,
            quantity integer,
            primary key(order_id)
        )
        """,
    )

    show_orders_task = PythonOperator(
        task_id="show_orders", python_callable=show_orders
    )

    write_orders_csv_task = PythonOperator(
        task_id="write_orders_csv", python_callable=write_orders_csv
    )

    # dag setup
    (maybe_create_table >> show_orders_task >> write_orders_csv_task)
