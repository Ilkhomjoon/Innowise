import psycopg2
from psycopg2.extras import execute_batch
from typing import List
import logging

# Logging sozlash
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseManager:
    def __init__(self, host: str, database: str, user: str, password: str, port: int = 5432):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.connection = None
        self.cursor = None
    
    def connect(self) -> None:
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )
            self.cursor = self.connection.cursor()
            logger.info(f"✓ Database ga muvaffaqiyatli ulanildi: {self.database}")
        except psycopg2.Error as e:
            logger.error(f"✗ Database ga ulanishda xatolik: {e}")
            raise
    
    def disconnect(self) -> None:
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            logger.info("✓ Database dan uzilindi")
    
    def execute_query(self, query: str, params: tuple = None) -> None:
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
        except psycopg2.Error as e:
            self.connection.rollback()
            logger.error(f"✗ So'rov bajarishda xatolik: {e}")
            raise
    
    def fetch_all(self, query: str, params: tuple = None) -> List[tuple]:
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            logger.error(f"✗ Ma'lumot olishda xatolik: {e}")
            raise
    
    def execute_batch(self, query: str, data: List[tuple]) -> None:
        try:
            execute_batch(self.cursor, query, data, page_size=1000)
            self.connection.commit()
            logger.info(f"✓ {len(data)} ta yozuv yuklandi")
        except psycopg2.Error as e:
            self.connection.rollback()
            logger.error(f"✗ Batch yuklashda xatolik: {e}")
            raise
    
    def create_schema(self, schema_file: str) -> None:
        try:
            with open(schema_file, 'r', encoding='utf-8') as f:
                schema_sql = f.read()
            
            self.cursor.execute(schema_sql)
            self.connection.commit()
            logger.info("✓ Schema muvaffaqiyatli yaratildi")
        except FileNotFoundError:
            logger.error(f"✗ Fayl topilmadi: {schema_file}")
            raise
        except psycopg2.Error as e:
            self.connection.rollback()
            logger.error(f"✗ Schema yaratishda xatolik: {e}")
            raise
    
    def clear_tables(self) -> None:
        try:
            self.cursor.execute("TRUNCATE TABLE students, rooms CASCADE")
            self.connection.commit()
            logger.info("✓ Jadvallar tozalandi")
        except psycopg2.Error as e:
            self.connection.rollback()
            logger.error(f"✗ Jadvallarni tozalashda xatolik: {e}")
            raise
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()