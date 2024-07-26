from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator

# You should have set up your postgres database in the Setup page.
# Find the guide in Tutorials/Setup.md

default_args = {
    'owner': 'Bossixd',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    dag_id='postgres_dag',
    default_args=default_args,
    start_date=datetime(2024, 7, 25),
    schedule='0 0 * * *'
) as dag:
    # Create task 1 with PostgresOperator
    # This task will create a table called dag_runs
    task1 = PostgresOperator(
        task_id='create_postgres_table',
        postgres_conn_id='postgres_localhost', # Conn id found when creating connection in Admin --> Connection Page
        sql="""
            create table if not exists dag_runs (
                ds date,
                dag_id character varying,
                primary key (ds, dag_id)
            )
        """
    )

    # This task will delete any rows of data which are duplicates with the dag run we are going to insert
    # ds and dag.dag_id are airflow macros
    # ds is the date time
    # dag.dag_id is the dag id of the current DAG
    # Find out more about airflow macros: https://airflow.apache.org/docs/apache-airflow/1.10.10/macros-ref.html
    task2 = PostgresOperator(
        task_id='delete_dag_run',
        postgres_conn_id='postgres_localhost',
        sql="""
            delete from dag_runs where ds = '{{ ds }}' and dag_id = '{{ dag.dag_id }}';
        """
    )

    # This task will insert the current dag run information into dag_runs
    task3 = PostgresOperator(
        task_id='create_dag_run',
        postgres_conn_id='postgres_localhost',
        sql="""
            insert into dag_runs (ds, dag_id) values ('{{ ds }}', '{{ dag.dag_id }}');
        """
    )

    # Set dependency
    task1 >> task2 >> task3