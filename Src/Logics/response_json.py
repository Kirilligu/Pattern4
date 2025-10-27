from Src.Core.abstract_response import abstract_response
from Src.Core.validator import validator, operation_exception
from Src.Logics.Convertors.convert_factory import convert_factory
import json


class response_json(abstract_response):
    """
    Класс для формирования ответа в формате JSON
    """

    def build(self, format: str, data: list) -> str:
        text = super().build(format, data)

        try:
            factory = convert_factory()
            result_data = []

            for item in data:
                # Конвертируем каждый объект через фабрику
                converted_item = factory.convert(item)
                result_data.append(converted_item)

            return json.dumps(result_data, ensure_ascii=False, indent=2)

        except Exception as error:
            raise operation_exception(f"Ошибка преобразования в JSON: {str(error)}")