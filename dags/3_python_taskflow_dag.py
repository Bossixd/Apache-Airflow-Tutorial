from datetime import datetime, timedelta

from airflow.decorators import dag, task

default_args = {
    'owner': 'Pattkit',
    'retries': 5,
    'retry_delay': timedelta(minutes=2),
}

@dag(
    dag_id='python_taskflow_dag',
    default_args=default_args,
    start_date=datetime(2024, 7, 24, 2),
    schedule_interval='@daily'
)
def hello_world_etl():
    @task(multiple_outputs=True)
    def get_name():
        return {
            'first_name': 'Pattakit',
            'last_name': 'Charoensedtakul'
        }

    @task()
    def get_age():
        return 20
    
    @task()
    def greet(first_name, last_name, age):
        print(f'My name is {first_name} {last_name}, and I am {age} years old.')

    name_dict = get_name()
    age = get_age()
    greet(
        first_name=name_dict['first_name'], 
        last_name=name_dict['last_name'], 
        age=age
    )

greet_dag = hello_world_etl()