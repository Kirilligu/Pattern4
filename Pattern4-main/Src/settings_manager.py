from Src.Models.settings_model import settings_model
from Src.Core.validator import argument_exception, operation_exception, validator
from Src.Models.company_model import company_model
from Src.Core.common import common
import os
import json


class settings_manager:
    __full_file_name: str = ""
    __settings: settings_model = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(settings_manager, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.set_default()

    @property
    def settings(self) -> settings_model:
        return self.__settings

    @property
    def file_name(self) -> str:
        return self.__full_file_name

    @file_name.setter
    def file_name(self, value: str):
        validator.validate(value, str)
        full_file_name = os.path.abspath(value)
        if os.path.exists(full_file_name):
            self.__full_file_name = full_file_name.strip()
        else:
            raise argument_exception(f'Не найден файл настроек {full_file_name}')

    def load(self) -> bool:
        if self.__full_file_name == "":
            raise operation_exception("Не найден файл настроек!")

        try:
            with open(self.__full_file_name, 'r', encoding='utf-8') as file_instance:
                settings_data = json.load(file_instance)
                if "company" in settings_data:
                    company_data = settings_data["company"]
                    self._load_company_data(company_data)

                if "response_format" in settings_data:
                    response_format_value = settings_data["response_format"]
                    self.__settings.response_format = response_format_value

            return True

        except Exception as error:
            return False

    def _load_company_data(self, company_data: dict) -> bool:
        """
        Загрузить данные компании из словаря
        Аргументы:
            company_data (dict): Данные компании
        Возвращает:
            bool: True если загрузка успешна, False в противном случае
        """
        try:
            fields = common.get_fields(self.__settings.company)
            matching_keys = [key for key in company_data.keys() if key in fields]
            for key in matching_keys:
                setattr(self.__settings.company, key, company_data[key])

            return True
        except Exception:
            return False

    def set_default(self):

        company = company_model()
        company.name = "Рога и копыта"
        company.inn = -1

        self.__settings = settings_model()
        self.__settings.company = company
        self.__settings.response_format = "csv"