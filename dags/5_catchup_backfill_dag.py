from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'Bossixd',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

# Set start_date to a couple of days before your current date to see the full effect
# Try playing with catchup=True vs catchup=False
# Then, look at the DAG runs completed in the airflow user interface
with DAG(
    dag_id='catchup_backfill_dag',
    default_args=default_args,
    start_date=datetime(2024, 7, 20, 2),
    schedule_interval='@daily',
    catchup=False # Change this line to True
) as dag:
    task1 = BashOperator(
        task_id='task1',
        bash_command='echo This is a simple bash command'
    )