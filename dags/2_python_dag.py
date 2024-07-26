from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    "owner": "Bossixd",
    "retries": 5,
    "retry_delay": timedelta(minutes=2)
}

# Define greet function to print out first_name, last_name, and age
# This function will be used in the PythonOperator
def greet(first_name, last_name, age):
    print(f'Hello World! My name is {first_name} {last_name}, and I am {age} years old.')

with DAG(
    dag_id='python_dag',
    description='dag with python operator',
    start_date=datetime(2024, 7, 23, 2),
    schedule_interval='@daily',
    default_args=default_args
) as dag:
    # Create Task1
    # This task will print out the first_name, last_name, and age
    task1 = PythonOperator(
        task_id='greet',
        python_callable=greet,
        op_kwargs={
            'first_name': 'John',
            'last_name': 'Doe',
            'age': 20
        }
    )

    task1