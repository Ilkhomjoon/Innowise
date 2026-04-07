from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'innowise_trainee',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'snowflake_airline_etl',
    default_args=default_args,
    description='Snowflake DWH ETL Pipeline using Airflow',
    start_date=datetime(2023, 10, 1),
    schedule='@daily',
    catchup=False
) as dag:

    # Load data into raw layer
    load_stage1 = SQLExecuteQueryOperator(
        task_id='load_stage1_raw',
        conn_id='snowflake_default',
        sql="CALL AIRLINE_DWH.STAGE_1_RAW.LOAD_RAW_DATA();",
        autocommit=True
    )

    # Loading data with help of stream into core layer
    process_stage2 = SQLExecuteQueryOperator(
        task_id='process_stage2_core',
        conn_id='snowflake_default',
        sql="CALL AIRLINE_DWH.STAGE_2_CORE.PROCESS_CORE_DATA();",
        autocommit=True
    )

    # Update analytics layer
    process_stage3 = SQLExecuteQueryOperator(
        task_id='process_stage3_analytics',
        conn_id='snowflake_default',
        sql="CALL AIRLINE_DWH.STAGE_3_ANALYTICS.PROCESS_ANALYTICS_DATA();",
        autocommit=True
    )

    load_stage1 >> process_stage2 >> process_stage3