from datetime import datetime
from airflow import DAG
from airflow.operators.email import EmailOperator

default_args = {
    "owner": "multionos",
}

with DAG(
    dag_id="email_test",
    default_args=default_args,
    start_date=datetime(2025, 2, 19),
    schedule_interval=None,
) as dag:
    task = EmailOperator(
        task_id="sendmail",
        to="test@example.com",
        subject="Airflow test send mail",
        html_content="<p>this is a test</p>",
    )

    task
