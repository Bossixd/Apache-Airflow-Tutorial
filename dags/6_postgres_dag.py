from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator

default_args = {
    'owner': 'Pattakit',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    dag_id='postgres_dag',
    default_args=default_args,
    start_date=datetime(2024, 7, 25),
    schedule='0 0 * * *'
) as dag:
    task1 = PostgresOperator(
        task_id='create_postgres_table',
        postgres_conn_id='postgres_localhost',
        sql="""
            create table if not exists dag_runs (
                ds date,
                dag_id character varying,
                primary key (ds, dag_id)
            )
        """
    )

    task2 = PostgresOperator(
        task_id='delete_dag_run',
        postgres_conn_id='postgres_localhost',
        sql="""
            delete from dag_runs where ds = '{{ ds }}' and dag_id = '{{ dag.dag_id }}';
        """
    )

    task3 = PostgresOperator(
        task_id='create_dag_run',
        postgres_conn_id='postgres_localhost',
        sql="""
            insert into dag_runs (ds, dag_id) values ('{{ ds }}', '{{ dag.dag_id }}');
        """
    )

    task1 >> task2 >> task3