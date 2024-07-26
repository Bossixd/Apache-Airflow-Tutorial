# Download and setup Apache Airflow
Setup guide can be found [here](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)
1. Load image
>>>
    curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.9.3/docker-compose.yaml'
    mkdir -p ./dags ./logs ./plugins ./config
    echo -e "AIRFLOW_UID=$(id -u)" > .env
>>>

2. Create Dockerfile and requirements.txt

Dockerfile:
>>>
    FROM apache/airflow:2.9.3
    COPY requirements.txt requirements.txt
    RUN pip install --upgrade pip
    RUN pip install --no-cache-dir -r requirements.txt
>>>

requirements.txt (this file can be empty)
>>>
    package1
    package2==1.0.0
    ...
>>>

3. Build airflow with requirements image
>>>
    docker build . --tag extended_airflow:latest
>>>

4. Edit docker-compose file

Change
>>>
    image: ${AIRFLOW_IMAGE_NAME:-apache/airflow:2.9.3}
>>>

To
>>>
    image: extended_airflow:latest
>>>

# Host PostGres database on docker
This will be required for exercise 7. You can skip this until later.
1. Add ports to postgres settings in docker-compose
```
    services:
    postgres:
        image: postgres:13
        environment:
        POSTGRES_USER: airflow
        POSTGRES_PASSWORD: airflow
        POSTGRES_DB: airflow
        volumes:
            - postgres-db-volume:/var/lib/postgresql/data
```
Add ports here:
```
        ports:
            - 5432:5432
```
2. Reload postgres database or recompose airflow
>>>
    docker compose up -d --build postgres 
>>>

3. Connect to database using dbeaver
    - Add connection
        - Host: localhost
        - Port: 5432
        - Database: postgres
        - Username: airflow
        - Password: airflow

4. Create database called table in dbeaver
    - Right click **Databases** and press create table
    - Set table name as **test**

4. Add database to airflow
    - Go to **Admins** in the top bar and select **Connections**
    - Press **+** to add new record
        - Connection Id: postgres_localhost
        - Connection Type: Postgres
        - Host
            - mac: host.docker.internal
            - windows: localhost 
        - Database: test
        - Login: airflow
        - Password: airflow
        - Port: 5432

# Host Minio S3 on docker
This will be required for exercise 8 and 9. You can skip this until later. \
[Tutorial](https://collabnix.com/running-minio-using-docker-desktop-in-5-minutes/) \
[AWS Provider Docs](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/index.html) \
[AWS Provider Subpackages](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/_api/airflow/providers/amazon/index.html)

1. On a seperate terminal, run
>>>
    docker run \
        -p 9000:9000 \
        -p 9001:9001 \
        -e "MINIO_ROOT_USER=admin" \
        -e "MINIO_ROOT_PASSWORD=password" \
        minio/minio server /data --console-address ":9001" 
>>>

2. Get airflow-webserver id. Either check docker desktip or run `docker ps`
3. Run `docker exec -it [DOCKER_ID] bash`
4. Run `pip list grep amazon`
5. Login to Minio
    - username: admin
    - password: password
6. Create Access Key
    - Go to **Access Keys** in the side bar
    - Press **Create Access Key**
    - Copy down the **Access Key** and **Secret Access Key**
5. Add Minio S3 to airflow
    - Go to **Admins** in the top bar and select **Connections**
    - Press **+** to add new record
        - Connection Id: minio_localhost
        - Connection Type: Amazon Web Services
        - AWS Access Key ID: admin
        - AWS Secret Access Key: password
        - Extra: 
>>>
    {
        "aws_access_key_id": "3m4TW0TPnnMWUYqht1c7",
        "aws_secret_access_key": "ieRvSoh2s91wzZcD7Iz3x1cMmH3JNwAcEIdlB2sM",
        "endpoint_url": "http://host.docker.internal:9000"
    }
>>>

# Run Apache Airflow
1. Build Image with requirements
>>>
    docker build . --tag extended_airflow:latest
>>>

2. Compose airflow-init
>>>
    docker compose up airflow-init
>>>

3. Compose apache airflow
>>>
    docker compose up -d
>>>

4. Cleaning up
>>>
    docker compose down -v
>>>