from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'Bossixd',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

# Set start_date to a month before your current date to see the full effect
# Try playing with the schedule_interval using cron schedule expressions
# Test out cron schedule expressions here: https://crontab.guru/
# Try out:
# 0 0 * * *
# 0 0 1,8,15,22 * *
# 0 3 * * *
# 0 3 * * Tue
# 0 3 * * Tue,Wed,Thurs,Fri
# 0 3 * * Tue-Fri
with DAG(
    dag_id='cron_format_dag',
    default_args=default_args,
    start_date=datetime(2024, 7, 1),
    schedule_interval='0 3 * * Tue-Fri', # Replace with your cron expression
    catchup=True
) as dag:
    task1 = BashOperator(
        task_id='task1',
        bash_command='echo dag with cron expression'
    )
    task1