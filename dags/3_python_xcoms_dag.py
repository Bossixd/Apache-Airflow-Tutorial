from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    "owner": "Bossixd",
    "retries": 5,
    "retry_delay": timedelta(minutes=2)
}

# Define get_name function to push first_name and last_name to xcom
def get_name(ti):
    ti.xcom_push(key='first_name', value='John')
    ti.xcom_push(key='last_name', value='Doe')

# Define get_age function to push age to xcom
def get_age(ti):
    ti.xcom_push(key='age', value=17)

# Define greet function to print out first_name, last_name, and age
def greet(ti):
    # Pull first_name and last_name from xcom
    first_name = ti.xcom_pull(task_ids='get_name', key='first_name')
    last_name = ti.xcom_pull(task_ids='get_name', key='last_name')
    age = ti.xcom_pull(task_ids='get_age', key='age')
    print(f'Hello World! My name is {first_name} {last_name}, and I am {age} years old.')

with DAG(
    dag_id='python_dag',
    description='dag with python operator',
    start_date=datetime(2024, 7, 23, 2),
    schedule_interval='@daily',
    default_args=default_args
) as dag:
    # Create task 1
    # This task will call the greet function to print the name and age
    task1 = PythonOperator(
        task_id='greet',
        python_callable=greet,
    )

    # Create task 2
    # This task will push name to xcom
    task2 = PythonOperator(
        task_id='get_name',
        python_callable=get_name
    )

    # Create task 3
    # This task will push age to xcom
    task3 = PythonOperator(
        task_id='get_age',
        python_callable=get_age
    )

    # Since task 1 will need to come after we have pushed both the names and age to xcom
    # We will set the dependencies as task 1 is the downstream of both task 2 and task 3
    #
    # Task 2 --\
    #           \
    #            > Task 1
    #           /
    # Task 3 --/
    #

    [task2, task3] >> task1
