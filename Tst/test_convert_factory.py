import unittest
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from Src.Logics.Convertors.convert_factory import convert_factory
from Src.Core.entity_model import entity_model
from Src.Logics.Convertors.datetime_convertor import datetime_convertor
from Src.Logics.Convertors.reference_convertor import reference_convertor
from Src.Logics.Convertors.basic_convertor import basic_convertor
from datetime import datetime

class test_convert_factory(unittest.TestCase):
    """
    Тесты для фабрики конвертеров
    """
    def test_convert_factory_datetime(self):
        # Подготовка
        factory = convert_factory()
        test_date = datetime(2023, 12, 25, 14, 30, 0)

        # Действие - фабрика возвращает конвертер, затем конвертируем
        converter = factory.create(test_date)
        result = converter.convert(test_date)
        #проверка
        self.assertIsInstance(converter, datetime_convertor)
        self.assertIn('datetime', result)

    def test_convert_factory_model(self):
        #подготовка
        factory = convert_factory()
        test_model = entity_model()
        test_model.name = "Тест"

        # Действие - фабрика возвращает конвертер, затем конвертируем
        converter = factory.create(test_model)
        result = converter.convert(test_model)
        # Проверка
        self.assertIsInstance(converter, reference_convertor)
        self.assertIn('id', result)
        self.assertEqual(result['name'], "Тест")

    def test_convert_factory_simple(self):
        # Подготовка
        factory = convert_factory()
        test_string = "Простая строка"

        # Действие - фабрика возвращает конвертер, затем конвертируем
        converter = factory.create(test_string)
        result = converter.convert(test_string)
        # Проверка
        self.assertIsInstance(converter, basic_convertor)
        self.assertEqual(result['name'], "Простая строка")

if __name__ == '__main__':
    unittest.main()