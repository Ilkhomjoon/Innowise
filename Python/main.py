#!/usr/bin/env python3
"""
BigData Python Module - Final Project
Muallif: [Ismingiz]
Sana: 2024

Bu dastur rooms va students ma'lumotlarini PostgreSQL bazasiga yuklaydi
va turli statistik hisoblarni chiqaradi.
"""

import argparse
import sys
import os
import logging
from typing import Optional

# Src modullarini import qilish
from src.database import DatabaseManager
from src.data_loader import DataLoader
from src.queries import QueryExecutor
from src.formatter import ResultFormatter
from src.indexes import IndexManager

# Logging sozlash
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('bigdata_app.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)


class BigDataApp:
    """
    Asosiy application klassi.
    SOLID: Single Responsibility - faqat dastur oqimini boshqarish.
    """
    
    def __init__(self, config: dict):
        """
        Args:
            config: Database va boshqa sozlamalar
        """
        self.config = config
        self.db_manager: Optional[DatabaseManager] = None
        self.data_loader: Optional[DataLoader] = None
        self.query_executor: Optional[QueryExecutor] = None
        self.index_manager: Optional[IndexManager] = None
    
    def initialize(self) -> None:
        """Dasturni ishga tushirish."""
        logger.info("=" * 70)
        logger.info("BIGDATA APPLICATION ISHGA TUSHDI")
        logger.info("=" * 70)
        
        # Database Manager yaratish
        self.db_manager = DatabaseManager(
            host=self.config['db_host'],
            database=self.config['db_name'],
            user=self.config['db_user'],
            password=self.config['db_password'],
            port=self.config['db_port']
        )
        
        # Database ga ulanish
        self.db_manager.connect()
        
        # Boshqa komponentlarni yaratish
        self.data_loader = DataLoader(self.db_manager)
        self.query_executor = QueryExecutor(self.db_manager)
        self.index_manager = IndexManager(self.db_manager)
    
    def setup_schema(self) -> None:
        """Database schema yaratish."""
        logger.info("Schema yaratish boshlandi...")
        
        schema_file = 'sql/schema.sql'
        if os.path.exists(schema_file):
            self.db_manager.create_schema(schema_file)
        else:
            logger.warning(f"Schema fayl topilmadi: {schema_file}")
    
    def load_data(self, rooms_path: str, students_path: str) -> None:
        """
        Ma'lumotlarni yuklash.
        
        Args:
            rooms_path: rooms.json fayl yo'li
            students_path: students.json fayl yo'li
        """
        # Fayllar mavjudligini tekshirish
        if not os.path.exists(rooms_path):
            raise FileNotFoundError(f"Rooms fayli topilmadi: {rooms_path}")
        
        if not os.path.exists(students_path):
            raise FileNotFoundError(f"Students fayli topilmadi: {students_path}")
        
        # Ma'lumotlarni yuklash
        stats = self.data_loader.load_all(rooms_path, students_path)
        
        logger.info(f"Yuklandi: {stats['rooms']} xona, {stats['students']} talaba")
    
    def create_indexes(self) -> None:
        """Indekslarni yaratish."""
        self.index_manager.create_indexes()
    
    def execute_queries(self) -> dict:
        """Barcha so'rovlarni bajarish."""
        return self.query_executor.execute_all_queries()
    
    def save_results(self, results: dict, output_format: str, output_file: str) -> None:
        """
        Natijalarni saqlash.
        
        Args:
            results: Query natijalari
            output_format: 'json' yoki 'xml'
            output_file: Chiqish fayli yo'li
        """
        formatter = ResultFormatter()
        
        # Formatga ko'ra konvertatsiya qilish
        if output_format.lower() == 'json':
            content = formatter.to_json(results)
        elif output_format.lower() == 'xml':
            content = formatter.to_xml(results)
        else:
            raise ValueError(f"Noto'g'ri format: {output_format}. 'json' yoki 'xml' bo'lishi kerak.")
        
        # Faylga saqlash
        formatter.save_to_file(content, output_file)
        
        # Konsolda xulosani ko'rsatish
        formatter.print_summary(results)
        
        logger.info(f"Natijalar saqlandi: {output_file}")
    
    def run(self, rooms_path: str, students_path: str, output_format: str = 'json') -> None:
        """
        Dasturni to'liq ishga tushirish.
        
        Args:
            rooms_path: rooms.json fayl yo'li
            students_path: students.json fayl yo'li
            output_format: Chiqish formati ('json' yoki 'xml')
        """
        try:
            # 1. Initialization
            self.initialize()
            
            # 2. Schema yaratish (agar kerak bo'lsa)
            if self.config.get('create_schema', False):
                self.setup_schema()
            
            # 3. Ma'lumotlarni yuklash
            self.load_data(rooms_path, students_path)
            
            # 4. Indekslarni yaratish
            self.create_indexes()
            
            # 5. So'rovlarni bajarish
            results = self.execute_queries()
            
            # 6. Natijalarni saqlash
            output_file = f"results.{output_format}"
            self.save_results(results, output_format, output_file)
            
            logger.info("=" * 70)
            logger.info("DASTUR MUVAFFAQIYATLI YAKUNLANDI!")
            logger.info("=" * 70)
            
        except Exception as e:
            logger.error(f"✗ Dastur xatosi: {e}", exc_info=True)
            raise
        
        finally:
            # Database dan uzilish
            if self.db_manager:
                self.db_manager.disconnect()
    
    def cleanup(self) -> None:
        """Tozalash (test uchun)."""
        if self.db_manager:
            self.db_manager.clear_tables()


def parse_arguments():
    """Command line argumentlarini parse qilish."""
    parser = argparse.ArgumentParser(
        description='BigData Python Module - Rooms va Students ma\'lumotlarini yuklash va tahlil qilish',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Misollar:
  python main.py --students data/students.json --rooms data/rooms.json --format json
  python main.py -s data/students.json -r data/rooms.json -f xml
  python main.py --students data/students.json --rooms data/rooms.json --create-schema
        """
    )
    
    parser.add_argument(
        '--students', '-s',
        type=str,
        required=True,
        help='Students JSON fayl yo\'li'
    )
    
    parser.add_argument(
        '--rooms', '-r',
        type=str,
        required=True,
        help='Rooms JSON fayl yo\'li'
    )
    
    parser.add_argument(
        '--format', '-f',
        type=str,
        choices=['json', 'xml'],
        default='json',
        help='Chiqish formati (default: json)'
    )
    
    parser.add_argument(
        '--create-schema',
        action='store_true',
        help='Schema yaratish (birinchi marta ishlatish uchun)'
    )
    
    parser.add_argument(
        '--db-host',
        type=str,
        default='localhost',
        help='Database host (default: localhost)'
    )
    
    parser.add_argument(
        '--db-name',
        type=str,
        default='students_db',
        help='Database nomi (default: bigdata_db)'
    )
    
    parser.add_argument(
        '--db-user',
        type=str,
        default='postgres',
        help='Database user (default: postgres)'
    )
    
    parser.add_argument(
        '--db-password',
        type=str,
        default='postgres',
        help='Database parol (default: postgres)'
    )
    
    parser.add_argument(
        '--db-port',
        type=int,
        default=5432,
        help='Database port (default: 5432)'
    )
    
    return parser.parse_args()


def main():
    """Asosiy funksiya."""
    # Argumentlarni parse qilish
    args = parse_arguments()
    
    # Konfiguratsiya yaratish
    config = {
        'db_host': args.db_host,
        'db_name': args.db_name,
        'db_user': args.db_user,
        'db_password': args.db_password,
        'db_port': args.db_port,
        'create_schema': args.create_schema
    }
    
    # Dasturni ishga tushirish
    app = BigDataApp(config)
    app.run(
        rooms_path=args.rooms,
        students_path=args.students,
        output_format=args.format
    )


if __name__ == '__main__':
    main()