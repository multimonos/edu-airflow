from datetime import datetime, timedelta
import csv
import logging
from airflow.operators.python import PythonOperator
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
import pendulum
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from os.path import basename

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


def write_then_upload_orders_csv(
    data_interval_end: pendulum.DateTime,
    data_interval_start: pendulum.DateTime,
) -> None:
    """write only order data within a specific run interval"""

    left = data_interval_start.format("YYYYMMDD")
    right = data_interval_end.format("YYYYMMDD")

    print(f"**** start: {left} ****")
    print(f"**** finish: {right} ****")
    print(f"**** select * from orders where date >= {left} and date < {right};")

    # get data
    hook = PostgresHook(postgres_conn_id=postgres_conn_id)
    conn = hook.get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "select * from orders where date >= %s and date < %s;",
        (left, right),
    )

    # write file
    ofile = f"/home/airflow/tmp/orders-{left}.csv"
    with open(ofile, "w+") as fp:
        writer = csv.writer(fp)
        print(f"cursor.description: {cursor.description}")
        writer.writerow([i[0] for i in cursor.description])
        writer.writerows(cursor)

    logging.info(f"orders : Wrote file {ofile}")
    cursor.close()
    conn.close()

    # upload file
    s3hook = S3Hook(aws_conn_id="devminio")
    s3key = basename(ofile)
    s3hook.load_file(filename=ofile, key=s3key, bucket_name="airflow-dev", replace=True)


# dag
default_args = {
    "owner": "multimonos",
    "retries": 5,
    "retry_delay": timedelta(minutes=10),
}

with DAG(
    dag_id="aws_s3_hook",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=True,
) as dag:
    """
    Preconditions,
    - i manually loaded the postgres-src/orders.csv vi psql using 'copy orders ... from ...' stmt

    This dag does the following,
    - create table in postgres
    - collect order data
    - write order data to file
    - upload file to s3 like bucket

    This example could be run via backfill as the order dates are historical, so, something like
    the following command would be effective in generating past csv files

    airflow dags backfill -s 2022-05-01 -e 2022-05-30 aws_s3_hook

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

    update_orders_csv_task = PythonOperator(
        task_id="write_then_upload_orders_csv",
        python_callable=write_then_upload_orders_csv,
    )

    # dag setup
    # todo could use python lib `tempfile` to write tmp instead persisting the tmp/orders*.csv files
    (maybe_create_table >> show_orders_task >> update_orders_csv_task)
