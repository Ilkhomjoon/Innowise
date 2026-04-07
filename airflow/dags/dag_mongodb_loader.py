import logging
import pandas as pd
from datetime import datetime
from airflow.decorators import dag, task
from airflow.providers.mongo.hooks.mongo import MongoHook
from config import PROCESSED_FILE_PATH, processed_dataset

log = logging.getLogger(__name__)

@dag(
    dag_id='2_load_to_mongodb_dag',
    start_date=datetime(2026, 1, 1),
    schedule=[processed_dataset],
    catchup=False
)
def load_to_mongodb_dag():

    @task()
    def load_to_mongo():
        hook = MongoHook(mongo_conn_id='mongo_default')
        client = hook.get_conn()
        db = client.innowise_db
        collection = db.airflow_data

        df = pd.read_csv(PROCESSED_FILE_PATH)
        records = df.to_dict(orient='records')

        if records:
            collection.insert_many(records)
            log.info("%d records successfully loaded into MongoDB.", len(records))
        else:
            log.info("No records found to load.")

    load_to_mongo()

load_to_mongodb_dag()