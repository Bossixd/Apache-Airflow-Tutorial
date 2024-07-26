# Exercise 1 | Your First DAG
In the DAGs folder, create a python file called `first_dag.py`. In this file, we will create a DAG with some simple tasks.

Open the file and import our dependencies:
```{python}
    from datetime import datetime, timedelta

    from airflow import DAG
    from airflow.operators.bash import BashOperator
```
`DAG` is an object in the airflow library, which will be used to create a DAG.

The datetime and timedelta objects will be used to set the DAG's start date and retry delays.