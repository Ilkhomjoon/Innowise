from airflow.datasets import Dataset

RAW_FILE_PATH = '/opt/airflow/data/airflow_data.csv'
PROCESSED_FILE_PATH = '/opt/airflow/data/processed_data.csv'
processed_dataset = Dataset(f"file://{PROCESSED_FILE_PATH}")

