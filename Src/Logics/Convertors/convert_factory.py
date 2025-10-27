from Src.Logics.Convertors.basic_convertor import basic_convertor
from Src.Logics.Convertors.datetime_convertor import datetime_convertor
from Src.Logics.Convertors.reference_convertor import reference_convertor
from Src.Core.abstract_model import abstact_model
from datetime import datetime

class convert_factory:
    """
    Фабрика конвертеров
    """
    def convert(self, obj):
        # Для даты используем datetime_convertor
        if isinstance(obj, datetime):
            converter = datetime_convertor()
            return converter.convert(obj)

        # Для моделей используем reference_convertor
        elif isinstance(obj, abstact_model):
            converter = reference_convertor()
            return converter.convert(obj)

        # Для всего остального используем basic_convertor
        else:
            converter = basic_convertor()
            return converter.convert(obj)