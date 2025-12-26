import json
from typing import List, Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class FileLoader:
    """
    JSON fayllarni o'qish va tekshirish uchun klass.
    SOLID: Single Responsibility - faqat fayl operatsiyalari.
    """
    
    @staticmethod
    def load_json(file_path: str) -> List[Dict[str, Any]]:
        """
        JSON faylni o'qish.
        
        Args:
            file_path: Fayl yo'li
            
        Returns:
            JSON ma'lumotlar ro'yxati
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            logger.info(f"✓ Fayl o'qildi: {file_path} ({len(data)} ta yozuv)")
            return data
        except FileNotFoundError:
            logger.error(f"✗ Fayl topilmadi: {file_path}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"✗ JSON formatida xatolik: {e}")
            raise
        except Exception as e:
            logger.error(f"✗ Kutilmagan xatolik: {e}")
            raise
    
    @staticmethod
    def validate_rooms(rooms: List[Dict[str, Any]]) -> bool:
        """
        Rooms ma'lumotlarini tekshirish.
        
        Args:
            rooms: Xonalar ro'yxati
            
        Returns:
            True - agar to'g'ri bo'lsa
        """
        required_fields = ['id', 'name']
        
        for idx, room in enumerate(rooms):
            for field in required_fields:
                if field not in room:
                    logger.error(f"✗ Room #{idx} da '{field}' maydoni yo'q")
                    return False
            
            if not isinstance(room['id'], int):
                logger.error(f"✗ Room #{idx} da 'id' integer bo'lishi kerak")
                return False
        
        logger.info("✓ Rooms ma'lumotlari to'g'ri")
        return True
    
    @staticmethod
    def validate_students(students: List[Dict[str, Any]]) -> bool:
        """
        Students ma'lumotlarini tekshirish.
        
        Args:
            students: Talabalar ro'yxati
            
        Returns:
            True - agar to'g'ri bo'lsa
        """
        required_fields = ['id', 'name', 'birthday', 'sex', 'room']
        
        for idx, student in enumerate(students):
            # Maydonlar mavjudligini tekshirish
            for field in required_fields:
                if field not in student:
                    logger.error(f"✗ Student #{idx} da '{field}' maydoni yo'q")
                    return False
            
            # ID tekshirish
            if not isinstance(student['id'], int):
                logger.error(f"✗ Student #{idx} da 'id' integer bo'lishi kerak")
                return False
            
            # Sex tekshirish
            if student['sex'] not in ['M', 'F']:
                logger.error(f"✗ Student #{idx} da 'sex' 'M' yoki 'F' bo'lishi kerak")
                return False
            
            # Birthday formatini tekshirish
            try:
                datetime.fromisoformat(student['birthday'])
            except ValueError:
                logger.error(f"✗ Student #{idx} da 'birthday' formati noto'g'ri")
                return False
        
        logger.info("✓ Students ma'lumotlari to'g'ri")
        return True


class DataTransformer:
    """
    Ma'lumotlarni database formatiga o'tkazish uchun klass.
    SOLID: Single Responsibility - faqat transformatsiya.
    """
    
    @staticmethod
    def transform_rooms(rooms: List[Dict[str, Any]]) -> List[tuple]:
        """
        Rooms ma'lumotlarini tuple formatiga o'tkazish.
        
        Args:
            rooms: Xonalar ro'yxati
            
        Returns:
            Tuple formatdagi ma'lumotlar
        """
        return [(room['id'], room['name']) for room in rooms]
    
    @staticmethod
    def transform_students(students: List[Dict[str, Any]]) -> List[tuple]:
        """
        Students ma'lumotlarini tuple formatiga o'tkazish.
        
        Args:
            students: Talabalar ro'yxati
            
        Returns:
            Tuple formatdagi ma'lumotlar
        """
        transformed = []
        for student in students:
            # Birthday ni datetime ga o'tkazish
            birthday = datetime.fromisoformat(student['birthday'])
            
            transformed.append((
                student['id'],
                student['name'],
                birthday,
                student['sex'],
                student['room']  # Bu room_id bo'ladi
            ))
        
        return transformed