import logging
from .database import DatabaseManager

logger = logging.getLogger(__name__)


class IndexManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def create_indexes(self) -> None:
        logger.info("=" * 50)
        logger.info("INDEKSLARNI YARATISH BOSHLANDI")
        logger.info("=" * 50)
        
        indexes = [
            {
                'name': 'idx_students_room_id',
                'sql': 'CREATE INDEX IF NOT EXISTS idx_students_room_id ON students(room_id)',
                'description': 'Room ID bo\'yicha tez qidirish'
            },
            {
                'name': 'idx_students_birthday',
                'sql': 'CREATE INDEX IF NOT EXISTS idx_students_birthday ON students(birthday)',
                'description': 'Birthday bo\'yicha yosh hisoblashni tezlashtirish'
            },
            {
                'name': 'idx_students_sex',
                'sql': 'CREATE INDEX IF NOT EXISTS idx_students_sex ON students(sex)',
                'description': 'Jins bo\'yicha filtrlashni tezlashtirish'
            },
            {
                'name': 'idx_students_room_sex',
                'sql': 'CREATE INDEX IF NOT EXISTS idx_students_room_sex ON students(room_id, sex)',
                'description': 'Composite indeks: room_id va sex (Query 4 uchun)'
            },
            {
                'name': 'idx_students_room_birthday',
                'sql': 'CREATE INDEX IF NOT EXISTS idx_students_room_birthday ON students(room_id, birthday)',
                'description': 'Composite indeks: room_id va birthday (Query 2,3 uchun)'
            }
        ]
        
        for idx in indexes:
            try:
                self.db_manager.execute_query(idx['sql'])
                logger.info(f"✓ {idx['name']} yaratildi - {idx['description']}")
            except Exception as e:
                logger.error(f"✗ {idx['name']} yaratishda xatolik: {e}")
                raise
        
        logger.info("=" * 50)
        logger.info("BARCHA INDEKSLAR YARATILDI")
        logger.info("=" * 50)
    
    def drop_indexes(self) -> None:
        logger.info("Indekslarni o'chirish boshlandi...")
        
        indexes = [
            'idx_students_room_id',
            'idx_students_birthday',
            'idx_students_sex',
            'idx_students_room_sex',
            'idx_students_room_birthday'
        ]
        
        for idx_name in indexes:
            try:
                self.db_manager.execute_query(f'DROP INDEX IF EXISTS {idx_name}')
                logger.info(f"✓ {idx_name} o'chirildi")
            except Exception as e:
                logger.error(f"✗ {idx_name} o'chirishda xatolik: {e}")
    
    def get_index_info(self) -> list:
        """Indekslar haqida ma'lumot olish."""
        query = """
            SELECT 
                tablename,
                indexname,
                indexdef
            FROM pg_indexes
            WHERE schemaname = 'public'
            ORDER BY tablename, indexname
        """
        
        return self.db_manager.fetch_all(query)
    
    def print_index_statistics(self) -> None:
        print("\n" + "=" * 60)
        print("INDEKSLAR STATISTIKASI")
        print("=" * 60)
        
        indexes = self.get_index_info()
        
        for idx in indexes:
            print(f"\nJadval: {idx[0]}")
            print(f"Indeks: {idx[1]}")
            print(f"Ta'rif: {idx[2]}")
        
        print("\n" + "=" * 60)