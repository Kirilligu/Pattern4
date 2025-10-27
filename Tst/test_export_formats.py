import unittest
import os
from Src.start_service import start_service
from Src.Logics.factory_entities import factory_entities
from Src.reposity import reposity


class test_export_formats(unittest.TestCase):
    """
    Тестовый класс для проверки генерации данных в различных форматах
    """
    def test_generate_all_formats(self):
        """
        Тестирование генерации данных во всех поддерживаемых форматах
        Проверяет создание файлов экспорта и их содержимое
        """
        # Инициализация сервиса и загрузка данных
        service_instance = start_service()
        service_instance.start()
        # Получение тестовых данных
        test_data = service_instance.data[reposity.range_key()]
        # Создание фабрики для генерации форматов
        entity_factory = factory_entities()
        # Список форматов
        supported_formats = ["csv", "markdown", "json", "xml"]
        for format_type in supported_formats:
            format_handler_class = entity_factory.create(format_type)
            format_handler_instance = format_handler_class()
            generated_content = format_handler_instance.build(format_type, test_data)
            export_filename = f"export_{format_type}.txt"
            with open(export_filename, "w", encoding="utf-8") as file_handler:
                file_handler.write(generated_content)

            # Проверка что файл был создан и содержит данные
            file_exists = os.path.exists(export_filename)
            has_content = len(generated_content) > 0
            self.assertTrue(file_exists, f"Файл {export_filename} не был создан")
            self.assertTrue(has_content, f"Файл {export_filename} пустой")


if __name__ == '__main__':
    unittest.main()