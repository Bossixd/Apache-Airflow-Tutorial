import csv
import logging
from datetime import datetime, timedelta
from tempfile import NamedTemporaryFile

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

# You should have set up your postgres database and minio S3 in the Setup page,
# import data into your postgres database, and
# created a bucket called airflow
# Find the general guide in Tutorials/Setup.md
# For more specific guides, go to Tutorials/9_postgres_to_s3_dag.md

default_args = {
    'onwer': 'Bossixd',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

# Create a function transfer data from postgres database to s3 bucket in minio
def postgres_to_s3(ts):
    # Step 1: query data from postgres database -------------------------

    # Create a Postgres hook to connect to the database
    hook = PostgresHook(postgres_conn_id='postgres_localhost')
    conn = hook.get_conn()
    cursor = conn.cursor()

    # Execute the select command to pull data from the postgres database
    cursor.execute("select * from public.orders where date <= '20220501'")

    # Create a temporary file to store this data
    # The suffix parameter will help us define each specific file when dealing with multiple files
    # ts is a airflow macro. You can add airflow macros to the function and airflow will automatically provide the parameter
    # Learn more about airflow macros: https://airflow.apache.org/docs/apache-airflow/1.10.10/macros-ref.html
    f = NamedTemporaryFile(mode='w', suffix=f"{ts}")

    # Create a csv writer
    csv_writer = csv.writer(f)

    # Write the data header into the txt file
    csv_writer.writerow([i[0] for i in cursor.description])

    # Write data into the txt file
    csv_writer.writerows(cursor)
    
    # Close connection to the postgres database
    cursor.close()
    conn.close()

    # Log that we have saved the data into a txt file
    logging.info('Saved orders data into text file: %s',  f'get_orders_{ts}.txt')

    # Step 2: upload text file to s3 -------------------------

    # Create a S3 Hook to minio S3
    s3_hook = S3Hook(aws_conn_id='minio_localhost')
    
    # load_file() will save the indicated file into minio S3
    s3_hook.load_file(
        filename=f.name,        # Name of file to be loaded
        key=f'orders/{ts}.txt', # Name of output file in minio S3 bucket
        bucket_name='airflow',  # Bucket name in minio S3
        replace=True            # Replace the output file if file already exists
    )

    # Log that we have saved the file to minio S3
    logging.info('File %s pushed to S3', f.name)

    # Close NamedTemporaryFile
    f.close()
    

with DAG(
    dag_id='8_postgres_to_s3_dag.py',
    default_args=default_args,
    start_date=datetime(2024, 7, 25),
    schedule_interval='0 0 * * *'
) as dag:
    task1 = PythonOperator(
        task_id='postgres_to_s3',
        python_callable=postgres_to_s3
    )

    task1