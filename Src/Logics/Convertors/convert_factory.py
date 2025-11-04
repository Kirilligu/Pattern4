from Src.Core.abstract_convertor import abstract_convertor
from Src.Logics.Convertors.basic_convertor import basic_convertor
from Src.Logics.Convertors.datetime_convertor import datetime_convertor
from Src.Core.abstract_model import abstact_model
from Src.Core.validator import operation_exception
from datetime import datetime

class convert_factory:
    """
    Фабрика для создания конвертеров
    """
    def create(self, obj) -> abstract_convertor:
        """
        Создает подходящий конвертер для объекта
        """
        if isinstance(obj, datetime):
            return datetime_convertor()
        elif isinstance(obj, abstact_model):
            from Src.Logics.Convertors.reference_convertor import reference_convertor
            return reference_convertor()
        elif isinstance(obj, (str, int, float, bool)) or obj is None:
            return basic_convertor()
        else:
            raise operation_exception(f"Неизвестный тип объекта: {type(obj)}")
