import os
import pandas as pd
from datetime import datetime
from airflow import DAG
from airflow.sensors.filesystem import FileSensor
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.task_group import TaskGroup
from airflow.datasets import Dataset

RAW_FILE_PATH = '/opt/airflow/data/airflow_data.csv'
PROCESSED_FILE_PATH = '/opt/airflow/data/processed_data.csv'

processed_dataset = Dataset(f"file://{PROCESSED_FILE_PATH}")

def check_file_empty():
    if not os.path.exists(RAW_FILE_PATH) or os.path.getsize(RAW_FILE_PATH) == 0:
        return 'log_empty_file'
    df = pd.read_csv(RAW_FILE_PATH)
    if df.empty:
        return 'log_empty_file'
    return 'processing_tasks.replace_nulls'

def replace_nulls_func():
    df = pd.read_csv(RAW_FILE_PATH)
    df.replace('null', '-', inplace=True)
    df.fillna('-', inplace=True)
    df.to_csv(PROCESSED_FILE_PATH, index=False)

def sort_data_func():
    df = pd.read_csv(PROCESSED_FILE_PATH)
    df['created_date'] = pd.to_datetime(df['created_date'])
    df.sort_values('created_date', inplace=True)
    df.to_csv(PROCESSED_FILE_PATH, index=False)

def clean_content_func():
    df = pd.read_csv(PROCESSED_FILE_PATH)
    df['content'] = df['content'].astype(str).str.replace(r'[^\w\s.,!?\'"-]', '', regex=True)
    df.to_csv(PROCESSED_FILE_PATH, index=False)

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
        bash_command='echo "Fayl bo\'sh! Ma\'lumot topilmadi."'
    )

    with TaskGroup("processing_tasks") as processing_group:
        replace_nulls = PythonOperator(task_id='replace_nulls', python_callable=replace_nulls_func)
        sort_data = PythonOperator(task_id='sort_data', python_callable=sort_data_func)
        clean_content = PythonOperator(
            task_id='clean_content', 
            python_callable=clean_content_func,
            outlets=[processed_dataset]
        )
        replace_nulls >> sort_data >> clean_content

    wait_for_file >> check_empty
    check_empty >> log_empty
    check_empty >> processing_group