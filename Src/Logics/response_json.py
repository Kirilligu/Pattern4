from Src.Core.abstract_response import abstract_response
from Src.Core.validator import validator, operation_exception
import json

class response_json(abstract_response):
    """
    Класс для формирования ответа в формате JSON
    """

    def build(self, format: str, data: list) -> str:
        """
        Сформировать JSON ответ из объектов данных
        Аргументы:
            format (str): Формат ответа (не используется в этой реализации)
            data (list): Список объектов данных для преобразования
        Возвращает:
            str: Строковое JSON представление данных
        Выбрасывает:
            operation_exception: Если преобразование данных завершилось ошибкой
        """
        text = super().build(format, data)

        try:
            result_data = self._convert_objects_to_dict(data)
            return json.dumps(result_data, ensure_ascii=False, indent=2)
        except Exception as error:
            raise operation_exception(f"Ошибка преобразования в JSON: {str(error)}")

    def _convert_objects_to_dict(self, data_objects: list) -> list:
        """
        Преобразовать список объектов в список словарей
        Аргументы:
            data_objects (list): Список объектов со свойствами
        Возвращает:
            list: Список словарей со свойствами объектов
        """
        converted_data = []

        for item in data_objects:
            # Получить все имена свойств из класса объекта
            property_names = self._get_object_properties(item)
            # Создать словарь со значениями свойств
            item_dict = {}
            for property_name in property_names:
                try:
                    property_value = getattr(item, property_name)
                    item_dict[property_name] = property_value
                except AttributeError:
                    continue
            converted_data.append(item_dict)

        return converted_data

    def _get_object_properties(self, target_object) -> list:
        """
        Извлечь имена свойств из класса объекта
        Аргументы:
            target_object: Объект для инспекции
        Возвращает:
            list: Список имен свойств
        """
        properties = []
        for attribute_name in dir(target_object.__class__):
            attribute = getattr(target_object.__class__, attribute_name)
            if isinstance(attribute, property):
                properties.append(attribute_name)

        return properties