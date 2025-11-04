from Src.Core.abstract_convertor import abstract_convertor
from Src.Core.abstract_model import abstact_model
from Src.Logics.Convertors.convert_factory import convert_factory

class reference_convertor(abstract_convertor):
    """
    Конвертер для ссылочных типов (Reference)
    """

    def convert(self, obj) -> dict:
        result = {}

        if isinstance(obj, abstact_model):
            factory = convert_factory()

            for attr_name in dir(obj):
                if attr_name.startswith('_'):
                    continue

                try:
                    attr_value = getattr(obj, attr_name)
                    converter = factory.create(attr_value)
                    result[attr_name] = converter.convert(attr_value)
                except:
                    continue

        return result