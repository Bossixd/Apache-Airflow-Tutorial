# Exercise 9 | Postgres to S3
1. Create database in postgres
    - Right click on **Databases** and press **Create New Database** with name test
    - Right click **test** database and set as default
2. Create table in postgres
>>>
    create table if not exists public.orders (
        order_id character varying, 
        date date,
        product_name character varying, 
        quantity integer, 
        primary key (order_id)
    )
>>>
3. Right click **test** database and import order.csv
4. Check if data is in the database by querying `select * from public.orders limit 100`