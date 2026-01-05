from typing import List, Dict, Any
import logging
from .database import DatabaseManager

logger = logging.getLogger(__name__)


class QueryExecutor:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def get_room_student_count(self) -> List[Dict[str, Any]]:
        query = """
            SELECT 
                r.id as room_id,
                r.name as room_name,
                COUNT(s.id) as student_count
            FROM rooms r
            LEFT JOIN students s ON r.id = s.room_id
            GROUP BY r.id, r.name
            ORDER BY r.id
        """
        
        logger.info("Executing Query 1: Room student count")
        results = self.db_manager.fetch_all(query)
        
        # Natijalarni dictionary formatiga o'tkazish
        formatted_results = []
        for row in results:
            formatted_results.append({
                'room_id': row[0],
                'room_name': row[1],
                'student_count': row[2]
            })
        
        logger.info(f"✓ {len(formatted_results)} ta xona topildi")
        return formatted_results
    
    def get_top_5_rooms_by_min_avg_age(self) -> List[Dict[str, Any]]:
        query = """
            SELECT 
                r.id as room_id,
                r.name as room_name,
                AVG(EXTRACT(YEAR FROM AGE(s.birthday))) as avg_age
            FROM rooms r
            INNER JOIN students s ON r.id = s.room_id
            GROUP BY r.id, r.name
            ORDER BY avg_age ASC
            LIMIT 5
        """
        
        logger.info("Executing Query 2: Top 5 rooms with youngest students")
        results = self.db_manager.fetch_all(query)
        
        formatted_results = []
        for row in results:
            formatted_results.append({
                'room_id': row[0],
                'room_name': row[1],
                'avg_age': float(row[2]) if row[2] else 0.0
            })
        
        logger.info(f"✓ {len(formatted_results)} ta xona topildi")
        return formatted_results
    
    def get_top_5_rooms_by_max_age_diff(self) -> List[Dict[str, Any]]:
        query = """
            SELECT 
                r.id as room_id,
                r.name as room_name,
                MAX(EXTRACT(YEAR FROM AGE(s.birthday))) - 
                MIN(EXTRACT(YEAR FROM AGE(s.birthday))) as age_diff
            FROM rooms r
            INNER JOIN students s ON r.id = s.room_id
            GROUP BY r.id, r.name
            ORDER BY age_diff DESC
            LIMIT 5
        """
        
        logger.info("Executing Query 3: Top 5 rooms with largest age difference")
        results = self.db_manager.fetch_all(query)
        
        formatted_results = []
        for row in results:
            formatted_results.append({
                'room_id': row[0],
                'room_name': row[1],
                'age_diff': float(row[2]) if row[2] else 0.0
            })
        
        logger.info(f"✓ {len(formatted_results)} ta xona topildi")
        return formatted_results
    
    def get_mixed_gender_rooms(self) -> List[Dict[str, Any]]:
        query = """
            SELECT DISTINCT
                r.id as room_id,
                r.name as room_name
            FROM rooms r
            INNER JOIN students s ON r.id = s.room_id
            GROUP BY r.id, r.name
            HAVING COUNT(DISTINCT s.sex) > 1
            ORDER BY r.id
        """
        
        logger.info("Executing Query 4: Mixed gender rooms")
        results = self.db_manager.fetch_all(query)
        
        formatted_results = []
        for row in results:
            formatted_results.append({
                'room_id': row[0],
                'room_name': row[1]
            })
        
        logger.info(f"✓ {len(formatted_results)} ta aralash xona topildi")
        return formatted_results
    
    def execute_all_queries(self) -> Dict[str, List[Dict[str, Any]]]:
        logger.info("=" * 50)
        logger.info("BARCHA SO'ROVLARNI BAJARISH BOSHLANDI")
        logger.info("=" * 50)
        
        results = {
            'room_student_count': self.get_room_student_count(),
            'top_5_youngest_rooms': self.get_top_5_rooms_by_min_avg_age(),
            'top_5_age_diff_rooms': self.get_top_5_rooms_by_max_age_diff(),
            'mixed_gender_rooms': self.get_mixed_gender_rooms()
        }
        
        logger.info("=" * 50)
        logger.info("BARCHA SO'ROVLAR BAJARILDI")
        logger.info("=" * 50)
        
        return results