import pandas as pd
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.datasets import Dataset
from airflow.providers.mongo.hooks.mongo import MongoHook

PROCESSED_FILE_PATH = '/opt/airflow/data/processed_data.csv'
processed_dataset = Dataset(f"file://{PROCESSED_FILE_PATH}")

def load_to_mongo_func():
    hook = MongoHook(mongo_conn_id='mongo_default')
    client = hook.get_conn()
    db = client.innowise_db
    collection = db.airflow_data
    
    df = pd.read_csv(PROCESSED_FILE_PATH)
    records = df.to_dict(orient='records')
    
    if records:
        collection.insert_many(records)
        print(f"{len(records)} ta yozuv MongoDB ga muvaffaqiyatli yuklandi.")

with DAG(
    dag_id='2_load_to_mongodb_dag',
    start_date=datetime(2023, 1, 1),
    schedule=[processed_dataset],
    catchup=False
) as dag:

    load_to_mongo = PythonOperator(
        task_id='load_to_mongo',
        python_callable=load_to_mongo_func
    )