import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)


class ResultFormatter:
    """
    Natijalarni JSON yoki XML formatida chiqarish uchun klass.
    SOLID: Single Responsibility - faqat formatlash.
    """
    
    @staticmethod
    def to_json(data: Dict[str, List[Dict[str, Any]]], indent: int = 2) -> str:
        """
        Ma'lumotlarni JSON formatiga o'tkazish.
        
        Args:
            data: Formatlash kerak bo'lgan ma'lumotlar
            indent: JSON indentatsiya (default: 2)
            
        Returns:
            JSON string
        """
        try:
            json_str = json.dumps(data, indent=indent, ensure_ascii=False)
            logger.info("✓ JSON formatiga o'tkazildi")
            return json_str
        except Exception as e:
            logger.error(f"✗ JSON ga o'tkazishda xatolik: {e}")
            raise
    
    @staticmethod
    def to_xml(data: Dict[str, List[Dict[str, Any]]]) -> str:
        """
        Ma'lumotlarni XML formatiga o'tkazish.
        
        Args:
            data: Formatlash kerak bo'lgan ma'lumotlar
            
        Returns:
            XML string
        """
        try:
            # Root element yaratish
            root = ET.Element("results")
            
            # Har bir query natijasini qo'shish
            for query_name, query_results in data.items():
                query_elem = ET.SubElement(root, "query")
                query_elem.set("name", query_name)
                
                # Har bir natijani qo'shish
                for item in query_results:
                    item_elem = ET.SubElement(query_elem, "item")
                    
                    # Har bir field ni qo'shish
                    for key, value in item.items():
                        field_elem = ET.SubElement(item_elem, key)
                        field_elem.text = str(value)
            
            # XML ni chiroyli formatga o'tkazish
            xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
            
            logger.info("✓ XML formatiga o'tkazildi")
            return xml_str
        except Exception as e:
            logger.error(f"✗ XML ga o'tkazishda xatolik: {e}")
            raise
    
    @staticmethod
    def save_to_file(content: str, file_path: str) -> None:
        """
        Natijani faylga saqlash.
        
        Args:
            content: Saqlanadigan kontent
            file_path: Fayl yo'li
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"✓ Natija saqlandi: {file_path}")
        except Exception as e:
            logger.error(f"✗ Faylga saqlashda xatolik: {e}")
            raise
    
    @staticmethod
    def print_summary(data: Dict[str, List[Dict[str, Any]]]) -> None:
        """
        Natijalarning qisqacha xulosasini chiqarish.
        
        Args:
            data: Natijalar
        """
        print("\n" + "=" * 60)
        print("NATIJALAR XULOSASI")
        print("=" * 60)
        
        for query_name, results in data.items():
            print(f"\n{query_name.upper()}:")
            print(f"  Natijalar soni: {len(results)}")
            
            if results:
                print(f"  Birinchi natija: {results[0]}")
        
        print("\n" + "=" * 60)