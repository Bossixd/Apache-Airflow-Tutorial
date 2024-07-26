from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

# Define Default Arguments for our DAG
default_args = {
    "owner": "Bossixd",
    "retries": 5,
    "retry_delay": timedelta(minutes=2)
}

# Initalize DAG using with statement
# Set dag_id, description, and start_date to anything you want
# datetime format is (year, month, day)
# Set schedule to '@daily' and default_args to default_args
with DAG(
    dag_id="1_first_dag",
    description="my first dag",
    start_date=datetime(2024, 7, 23),
    schedule_interval="@daily",
    default_args=default_args
) as dag:
    # Create task 1
    # This task will print out "hello world" in the terminal
    task1 = BashOperator(
        task_id="first_task",
        bash_command="echo hello world"
    )

    # Create Task 2
    # This task will print out some text in the terminal
    task2 = BashOperator(
        task_id="second_task",
        bash_command="echo hey, I am the second task and will run after first_task"
    )

    # Create Task 3
    # This task will print out some text in the terminal
    task3 = BashOperator(
        task_id="third_task",
        bash_command="echo hey i am task three"
    )

    # Let's set the dependencies of the tasks
    # Let Task1 be the first task in the workflow, followed by both Task2 and Task3
    #
    #          --> Task 2
    #         /
    # Task 1 < 
    #         \
    #          --> Task 3
    #

    # Method 1 : Using set_downstream() and set_upstream
    # task1.set_downstream(task2)
    # task3.set_upstream(task1)

    # Method 2 : Using >> operator
    task1 >> [task2, task3]
