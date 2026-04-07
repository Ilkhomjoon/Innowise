import os
import logging
import pandas as pd
from datetime import datetime
from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator
from airflow.sensors.filesystem import FileSensor
from airflow.operators.python import BranchPythonOperator
from airflow.utils.task_group import TaskGroup
from config import RAW_FILE_PATH, PROCESSED_FILE_PATH, processed_dataset

log = logging.getLogger(__name__)

def check_file_empty():
    if not os.path.exists(RAW_FILE_PATH) or os.path.getsize(RAW_FILE_PATH) == 0:
        return 'log_empty_file'
    df = pd.read_csv(RAW_FILE_PATH)
    if df.empty:
        return 'log_empty_file'
    return 'processing_tasks.replace_nulls'

@task()
def replace_nulls_func(raw_path: str, processed_path: str):
    df = pd.read_csv(raw_path)
    df.replace('null', '-', inplace=True)
    df.fillna('-', inplace=True)
    df.to_csv(processed_path, index=False)
    log.info("Null values replaced. Output written to %s", processed_path)

@task()
def sort_data_func(processed_path: str):
    df = pd.read_csv(processed_path)
    df['created_date'] = pd.to_datetime(df['created_date'])
    df.sort_values('created_date', inplace=True)
    df.to_csv(processed_path, index=False)
    log.info("Data sorted by created_date in %s", processed_path)

@task(outlets=[processed_dataset])
def clean_content_func(processed_path: str):
    df = pd.read_csv(processed_path)
    df['content'] = df['content'].astype(str).str.replace(r'[^\w\s.,!?\'"-]', '', regex=True)
    df.to_csv(processed_path, index=False)
    log.info("Content cleaned and saved to %s", processed_path)

with DAG(
    dag_id='1_data_processing_dag',
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False
) as dag:

    wait_for_file = FileSensor(
        task_id='wait_for_file',
        filepath=RAW_FILE_PATH,
        poke_interval=10,
        timeout=600
    )

    check_empty = BranchPythonOperator(
        task_id='check_file_empty',
        python_callable=check_file_empty
    )

    log_empty = BashOperator(
        task_id='log_empty_file',
        bash_command='echo "File is empty! No data found."'
    )

    with TaskGroup("processing_tasks") as processing_group:
        step1 = replace_nulls_func(RAW_FILE_PATH, PROCESSED_FILE_PATH)
        step2 = sort_data_func(PROCESSED_FILE_PATH)
        step3 = clean_content_func(PROCESSED_FILE_PATH)
        step1 >> step2 >> step3

wait_for_file >> check_empty >> [log_empty, processing_group]