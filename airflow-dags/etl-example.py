from airflow import DAG
from airflow.decorators import task
from airflow.utils.dates import days_ago


@task
def extract() -> str:
    return "raw order data"


@task
def transform(raw_data) -> str:
    return f"processed: {raw_data}"


@task
def validate(processed_data) -> str:
    return f"validated: {processed_data}"


@task
def load(validated_data) -> None:
    print(f"loaded all data: {validated_data}")


with DAG(
    dag_id="etlpipe",
    default_args={"start_date": days_ago(1)},
    schedule_interval="@daily",
    catchup=False,
) as dag:
    load_task = load(validate(transform(extract())))
