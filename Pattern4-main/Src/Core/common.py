from Src.Core.abstract_model import abstact_model
from Src.Core.validator import argument_exception


class common:
    """
    Набор общих методов
    """
    @staticmethod
    def get_models() -> list:
        result = []
        for inheritor in entity_model.__subclasses__():
            result.append(inheritor.__name__)
        return result

    @staticmethod
    def get_fields(source, is_common: bool = False) -> list:
        if source is None:
            raise argument_exception("Некорректно переданы аргументы!")

        items = list(filter(lambda x: not x.startswith("_"), dir(source)))
        result = []

        for item in items:
            attribute = getattr(source.__class__, item)
            if isinstance(attribute, property):
                value = getattr(source, item)

                # если нужно только простые поля
                if is_common and (isinstance(value, dict) or isinstance(value, list)):
                    continue

                result.append(item)

        return result

    """
    Получить все открытые атрибуты модели в виде словаря (для сохранения в файл)
    """
    @staticmethod
    def get_public_attributes(obj) -> dict:
        if obj is None:
            return {}

        data = {}
        fields = common.get_fields(obj, is_common=True)

        for field in fields:
            value = getattr(obj, field)
            if hasattr(value, "id"):
                data[field] = value.id
            else:
                data[field] = value

        return data