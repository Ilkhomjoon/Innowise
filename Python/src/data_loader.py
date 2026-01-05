from typing import Dict
import logging
from .database import DatabaseManager
from .loader import FileLoader, DataTransformer

logger = logging.getLogger(__name__)


class DataLoader:
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.file_loader = FileLoader()
        self.transformer = DataTransformer()
    
    def load_rooms(self, file_path: str) -> int:
        logger.info("=" * 50)
        logger.info("ROOMS MA'LUMOTLARINI YUKLASH BOSHLANDI")
        logger.info("=" * 50)
        
        rooms_data = self.file_loader.load_json(file_path)
        
        if not self.file_loader.validate_rooms(rooms_data):
            raise ValueError("Rooms ma'lumotlari noto'g'ri formatda")
        
        rooms_tuples = self.transformer.transform_rooms(rooms_data)
        
        insert_query = """
            INSERT INTO rooms (id, name)
            VALUES (%s, %s)
            ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name
        """
        
        self.db_manager.execute_batch(insert_query, rooms_tuples)
        
        logger.info(f"✓ {len(rooms_tuples)} ta xona yuklandi")
        return len(rooms_tuples)
    
    def load_students(self, file_path: str) -> int:
        logger.info("=" * 50)
        logger.info("STUDENTS MA'LUMOTLARINI YUKLASH BOSHLANDI")
        logger.info("=" * 50)
        students_data = self.file_loader.load_json(file_path)
        
        if not self.file_loader.validate_students(students_data):
            raise ValueError("Students ma'lumotlari noto'g'ri formatda")
        
        students_tuples = self.transformer.transform_students(students_data)
        
        insert_query = """
            INSERT INTO students (id, name, birthday, sex, room_id)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (id) DO UPDATE SET 
                name = EXCLUDED.name,
                birthday = EXCLUDED.birthday,
                sex = EXCLUDED.sex,
                room_id = EXCLUDED.room_id
        """
        
        self.db_manager.execute_batch(insert_query, students_tuples)
        
        logger.info(f"✓ {len(students_tuples)} ta talaba yuklandi")
        return len(students_tuples)
    
    def load_all(self, rooms_path: str, students_path: str) -> Dict[str, int]:
        logger.info("=" * 50)
        logger.info("MA'LUMOTLARNI YUKLASH JARAYONI BOSHLANDI")
        logger.info("=" * 50)
        
        stats = {}
        
        stats['rooms'] = self.load_rooms(rooms_path)
        
        # Keyin students ni yuklaymiz
        stats['students'] = self.load_students(students_path)
        
        logger.info("=" * 50)
        logger.info("YUKLASH YAKUNLANDI")
        logger.info(f"Jami yuklandi: {stats['rooms']} ta xona, {stats['students']} ta talaba")
        logger.info("=" * 50)
        
        return stats