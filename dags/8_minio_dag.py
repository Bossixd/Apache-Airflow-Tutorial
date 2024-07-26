from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor

# You should have set up your minio S3 in the Setup page,
# created a bucket called airflow, and
# inserted data.csv into this bucket
# Find the guide in Tutorials/Setup.md

default_args = {
    'owner': 'Bossixd',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    dag_id='minio_dag',
    default_args=default_args,
    start_date=datetime(2024, 7, 25),
    schedule='0 0 * * *'
) as dag:
    # Create task 1
    # This task will use the "poke" method to see if there is a file called "data.csv" in the "airflow" bucket
    task1 = S3KeySensor(
        task_id='minio_sensor',
        bucket_name='airflow',              # Bucket name found in Minio (airflow)
        bucket_key='data.csv',              # Data file name found in your bucket (data.csv)
        aws_conn_id='minio_localhost',      # Conn id found when creating connection in Admin --> Connection Page
        mode='poke',                        # Set mode to poke
        poke_interval=5,                    # Set poking interval to 5 seconds
        timeout=30                          # The task will timeout after 30 seconds have passed
    )

    task1

    # First, try running this DAG

    # Then try running it again, but without the data.csv file in the bucket

    # Finally, run the DAG. 
    # While the task is trying to find the file, observe how it cannot find the file. 
    # Then, add the file into the S3 bucket. 
    # The task will be completed successfully