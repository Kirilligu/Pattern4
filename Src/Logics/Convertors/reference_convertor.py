from Src.Core.abstract_convertor import abstract_convertor
from Src.Core.abstract_model import abstact_model

class reference_convertor(abstract_convertor):
    """
    Конвертер для ссылочных типов (Reference)
    """
    def convert(self, obj) -> dict:
        result = {}
        if isinstance(obj, abstact_model):
            # Берем только уникальный код как ссылку
            result['id'] = obj.unique_code
            result['name'] = getattr(obj, 'name', '')

        return result