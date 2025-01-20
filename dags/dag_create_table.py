from airflow.decorators import dag, task
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from datetime import datetime, timedelta
import os

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG using the @dag decorator
@dag(
    dag_id='dag_cr_table_snowflake',
    schedule_interval=None,  # No schedule for manual runs
    start_date=datetime(2025, 1, 1),
    catchup=False,
    default_args=default_args,
    tags=['snowflake'],
    template_searchpath=[os.path.join(os.path.dirname(os.path.abspath(__file__)), "../include/sql")],
    description="A DAG to run SQL queries Create table, Insert & display data from snowflake",
)
def cr_snowflake():

    # Task: Use SnowflakeOperator to run a SQL query
    create_table_query = SnowflakeOperator(
        task_id='create_table_query',
        snowflake_conn_id='snowflake_conn',  # Connection ID created in Airflow UI
        sql="create_table.sql",        # Example query
    )

    insert_data_query = SnowflakeOperator(
        task_id='insert_data_query',
        snowflake_conn_id='snowflake_conn',  # Connection ID created in Airflow UI
        sql="insert_data.sql",        # Example query
    )

    retrieve_data_query = SnowflakeOperator(
        task_id='retrieve_data_query',
        snowflake_conn_id='snowflake_conn',  # Connection ID created in Airflow UI
        sql="retrieve_data.sql",        # Example query
    )    

    # Additional Task: Example custom task using @task decorator
    @task
    def print_message():
        print("Snowflake query execution is complete!")

    # Task dependencies
    create_table_query >> insert_data_query >> retrieve_data_query >> print_message()

# Instantiate the DAG
dag_instance = cr_snowflake()