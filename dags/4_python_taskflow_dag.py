from datetime import datetime, timedelta

from airflow.decorators import dag, task

# The TaskFlow API is a functional API for using decorators to define DAGs and tasks, 
# which simplifies the process for passing data between tasks and defining dependencies.

default_args = {
    'owner': 'Bossixd',
    'retries': 5,
    'retry_delay': timedelta(minutes=2),
}

# Create our DAG using the dag decorator
@dag(
    dag_id='python_taskflow_dag',
    default_args=default_args,
    start_date=datetime(2024, 7, 24, 2),
    schedule_interval='@daily'
)
# Define function here which is decorated by @dag
def hello_world_etl():
    # Create our task using the task decorator
    # This get_name task will return the names of first_name and last_name
    # These values will automatically get sent to xcoms by taskflow API
    @task(multiple_outputs=True)
    def get_name():
        return {
            'first_name': 'John',
            'last_name': 'Doe'
        }

    # Create get_age task
    # This task will return the age
    @task()
    def get_age():
        return 20
    
    # Create greet task
    # This task will print out first_name, last_name, and age
    @task()
    def greet(first_name, last_name, age):
        print(f'My name is {first_name} {last_name}, and I am {age} years old.')

    # Create dependencies by just creating return variables and passing them to other functions
    name_dict = get_name()
    age = get_age()
    greet(
        first_name=name_dict['first_name'], 
        last_name=name_dict['last_name'], 
        age=age
    )

# Run the DAG
greet_dag = hello_world_etl()