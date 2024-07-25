from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "Pattakit",
    "retries": 5,
    "retry_delay": timedelta(minutes=2)
}

with DAG(
    dag_id="first_dag",
    description="my first dag",
    start_date=datetime(2024, 7, 23, 2),
    schedule="@daily",
    default_args=default_args
) as dag:
    task1 = BashOperator(
        task_id="first_task",
        bash_command="echo hello world"
    )

    task2 = BashOperator(
        task_id="second_task",
        bash_command="echo hey, I am the second task and will run after first_tasj"
    )

    task3 = BashOperator(
        task_id="third_task",
        bash_command="echo hey i am task three"
    )

    # task1.set_downstream(task2)
    # task1.set_downstream(task3)
    task1 >> [task2, task3]