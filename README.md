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

requirements.txt
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

# Host PostGres database on local machine
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
    - Goto **Admins** in the top bar and select **Connections**
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

# Run Apache Airflow
1. Build Image with requirements
>>>
    docker build . --tag extended_airflow:latest
>>>

2. Compose airflow-init (Only first time??? --> Read Tutorial)
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