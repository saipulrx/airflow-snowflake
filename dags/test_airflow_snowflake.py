from airflow.decorators import dag, task
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from datetime import datetime, timedelta

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG using the @dag decorator
@dag(
    dag_id='snowflake_dag_decorator_example',
    schedule_interval=None,  # No schedule for manual runs
    start_date=datetime(2025, 1, 1),
    catchup=False,
    default_args=default_args,
    description="A DAG to connect Airflow to Snowflake and run SQL queries",
)
def snowflake_dag():

    # Task: Use SnowflakeOperator to run a SQL query
    run_snowflake_query = SnowflakeOperator(
        task_id='run_snowflake_query',
        snowflake_conn_id='snowflake_conn',  # Connection ID created in Airflow UI
        sql="SELECT CURRENT_VERSION();",        # Example query
    )

    # Additional Task: Example custom task using @task decorator
    @task
    def print_message():
        print("Snowflake query execution is complete!")

    # Task dependencies
    run_snowflake_query >> print_message()

# Instantiate the DAG
dag_instance = snowflake_dag()