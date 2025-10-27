import unittest
import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from Src.Logics.Convertors.convert_factory import convert_factory
from Src.Core.entity_model import entity_model
from datetime import datetime

class test_convert_factory(unittest.TestCase):
    """
    Тесты для фабрики конвертеров
    """
    def test_convert_factory_datetime(self):
        # Подготовка
        factory = convert_factory()
        test_date = datetime(2023, 12, 25, 14, 30, 0)
        # Действие
        result = factory.convert(test_date)
        # Проверка
        self.assertIn('datetime', result)

    def test_convert_factory_model(self):
        # Подготовка
        factory = convert_factory()
        test_model = entity_model()
        test_model.name = "Тест"
        # Действие
        result = factory.convert(test_model)
        # Проверка
        self.assertIn('id', result)
        self.assertEqual(result['name'], "Тест")

    def test_convert_factory_simple(self):
        # Подготовка
        factory = convert_factory()

        class SimpleObject:
            def __init__(self):
                self.name = "Объект"
                self.value = 100

        test_obj = SimpleObject()
        # Действие
        result = factory.convert(test_obj)
        # Проверка
        self.assertEqual(result['name'], "Объект")
        self.assertEqual(result['value'], 100)

if __name__ == '__main__':
    unittest.main()