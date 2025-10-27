from abc import ABC, abstractmethod

class abstract_convertor(ABC):
    """
    Абстрактный класс конвертера объектов в словари
    """
    @abstractmethod
    def convert(self, obj) -> dict:
        """
        Конвертирует объект в словарь формата {наименование_поля: данные_поля}

        Args:
            obj: Любой объект для конвертации

        Returns:
            dict: Словарь с данными объекта
        """
        pass