from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator

default_args = {
    "owner": "multimonos",
    "retries": 5,
    "retry_delay": timedelta(minutes=10),
}

with DAG(
    dag_id="postgres_example",
    default_args=default_args,
    start_date=datetime(2025, 2, 17),
    schedule_interval="@daily",
) as dag:
    """
    This dag does the following,
    - maybe create table in postgres
    """
    task1 = PostgresOperator(
        task_id="maybe_create_table",
        postgres_conn_id="devpostgres",
        sql="""
        create table if not exists dag_runs (
            dt date,
            dag_id character varying,
            primary key (dt,dag_id)
        )
        """,
    )
