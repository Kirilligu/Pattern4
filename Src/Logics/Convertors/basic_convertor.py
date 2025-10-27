from Src.Core.abstract_convertor import abstract_convertor

class basic_convertor(abstract_convertor):
    """
    Конвертер для простых типов: числа и строки
    """

    def convert(self, obj) -> dict:
        result = {}
        # Просто берем все атрибуты объекта
        for attr_name in dir(obj):
            # Пропускаем служебные
            if attr_name.startswith('_'):
                continue
            try:
                value = getattr(obj, attr_name)

                # Если это строка или число - добавляем
                if isinstance(value, (str, int, float)):
                    result[attr_name] = value
            except:
                pass

        return result