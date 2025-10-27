from Src.Core.abstract_response import abstract_response
from Src.Core.common import common
from Src.Core.validator import validator, operation_exception

class response_xml(abstract_response):
    """
    Класс для формирования ответа в формате XML
    Преобразует объекты данных в структурированный XML документ
    """
    def build(self, format: str, data: list) -> str:
        """
        Сформировать XML документ из объектов данных
        Аргументы:
            format (str): Формат ответа
            data (list): Список объектов данных для преобразования
        Возвращает:
            str: XML документ в виде строки
        Выбрасывает:
            operation_exception: Если невозможно сформировать XML документ
        """
        text = super().build(format, data)

        try:
            xml_content = self._build_xml_document(data)
            return xml_content
        except Exception as error:
            raise operation_exception(f"Ошибка формирования XML документа: {str(error)}")

    def _build_xml_document(self, data: list) -> str:
        """
        Построить полный XML документ
        Аргументы:
            data (list): Список объектов данных
        Возвращает:
            str: Полный XML документ
        """
        xml_content = self._add_xml_declaration()
        xml_content += self._build_root_element(data)
        return xml_content

    def _add_xml_declaration(self) -> str:
        return '<?xml version="1.0" encoding="UTF-8"?>\n'

    def _build_root_element(self, data: list) -> str:
        root_content = "<items>\n"

        for data_item in data:
            root_content += self._build_item_element(data_item)

        root_content += "</items>\n"
        return root_content

    def _build_item_element(self, data_item) -> str:
        """
        Построить XML элемент для одного объекта данных
        Аргументы:
            data_item: Объект данных для преобразования
        Возвращает:
            str: XML элемент с полями объекта
        """
        item_content = "  <item>\n"
        field_names = common.get_fields(data_item)
        for field_name in field_names:
            item_content += self._build_field_element(field_name, data_item)
        item_content += "  </item>\n"
        return item_content

    def _build_field_element(self, field_name: str, data_item) -> str:
        """
        Построить XML элемент для одного поля объекта
        Аргументы:
            field_name (str): Название поля
            data_item: Объект данных
        Возвращает:
            str: XML элемент поля
        """
        try:
            field_value = str(getattr(data_item, field_name))
            return f"    <{field_name}>{field_value}</{field_name}>\n"
        except AttributeError:
            return f"    <{field_name}></{field_name}>\n"