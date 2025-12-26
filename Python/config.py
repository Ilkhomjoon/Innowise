"""
Konfiguratsiya sozlamalari.
Environment variables yoki default qiymatlardan foydalanadi.
"""
import os
from typing import Dict


class Config:
    """
    Dastur sozlamalari.
    SOLID: Single Responsibility - faqat konfiguratsiya.
    """
    
    # Database sozlamalari
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_NAME = os.getenv('DB_NAME', 'students_db')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '001106')
    DB_PORT = int(os.getenv('DB_PORT', '5432'))
    
    # Fayllar yo'li
    DATA_DIR = 'data'
    SQL_DIR = 'sql'
    OUTPUT_DIR = 'output'
    
    # Logging
    LOG_FILE = 'bigdata_app.log'
    LOG_LEVEL = 'INFO'
    
    @classmethod
    def get_db_config(cls) -> Dict[str, any]:
        """Database konfiguratsiyasini dictionary formatida qaytarish."""
        return {
            'host': cls.DB_HOST,
            'database': cls.DB_NAME,
            'user': cls.DB_USER,
            'password': cls.DB_PASSWORD,
            'port': cls.DB_PORT
        }
    
    @classmethod
    def validate(cls) -> bool:
        """Konfiguratsiyani tekshirish."""
        required = [cls.DB_HOST, cls.DB_NAME, cls.DB_USER, cls.DB_PASSWORD]
        return all(required)