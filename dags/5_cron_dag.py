from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'Pattakit',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    dag_id='cron_format_dag',
    default_args=default_args,
    start_date=datetime(2024, 7, 1),
    schedule_interval='0 3 * * Tue-Fri',
    catchup=True
) as dag:
    task1 = BashOperator(
        task_id='task1',
        bash_command='echo dag with cron expression'
    )
    task1