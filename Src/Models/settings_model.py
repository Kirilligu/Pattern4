from Src.Models.company_model import company_model
from Src.Core.validator import validator


class settings_model:
    """
    Модель настроек приложения
    Содержит настройки компании и форматы ответов
    """
    __company: company_model = None
    __response_format: str = "csv"

    @property
    def company(self) -> company_model:
        """
        Получить настройки компании
        Возвращает:
            company_model: Модель с данными компании
        """
        return self.__company

    @company.setter
    def company(self, value: company_model):
        """
        Установить настройки компании
        Аргументы:
            value (company_model): Модель с данными компании
        Выбрасывает:
            argument_exception: Если передана некорректная модель
        """
        validator.validate(value, company_model)
        self.__company = value

    @property
    def response_format(self) -> str:
        """
        Получить текущий формат ответа
        Возвращат:
            str: Формат ответа (csv, json, xml, markdown)
        """
        return self.__response_format

    @response_format.setter
    def response_format(self, value: str):
        """
        Установить формат ответа
        Аргументы:
            value (str): Название формата ответа
        Выбрасывает:
            argument_exception: Если передана некорректная строка
        """
        validator.validate(value, str)
        normalized_format = value.strip().lower()
        self.__response_format = normalized_format