from Src.Core.abstract_response import abstract_response
from Src.Logics.response_csv import response_csv
from Src.Logics.response_markdown import response_markdown
from Src.Logics.response_json import response_json
from Src.Logics.response_xml import response_xml
from Src.Core.validator import operation_exception
from Src.settings_manager import settings_manager


class factory_entities:
    __match = {
        "csv": response_csv,
        "markdown": response_markdown,
        "json": response_json,
        "xml": response_xml
    }

    __settings: settings_manager = None

    def __init__(self, settings: settings_manager = None):
        """
        Конструктор
        Args:
            settings (settings_manager): Менеджер настроек
        """
        if settings is None:
            self.__settings = settings_manager()
        else:
            self.__settings = settings

    def create(self, format: str) -> abstract_response:
        """
        Создать response по указанному формату
        Args:
            format (str): Формат ответа
        Returns:
            abstract_response: Объект для формирования ответа
        Raises:
            operation_exception: Некорректный формат
        """
        format = format.lower()
        if format not in self.__match:
            raise operation_exception("Формат не верный")
        return self.__match[format]()

    def create_default(self) -> abstract_response:
        """
        Создать response по формату из настроек
        Returns:
            abstract_response: Объект для формирования ответа
        """
        format = self.__settings.settings.response_format
        return self.create(format)

    @property
    def settings(self) -> settings_manager:
        """
        Менеджер настроек
        Returns:
            settings_manager: Менеджер настроек
        """
        return self.__settings