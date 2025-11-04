from Src.Core.abstract_response import abstract_response
from Src.Core.common import common
from Src.Core.validator import validator, operation_exception


class response_markdown(abstract_response):
    """
    Класс для формирования ответа в формате Markdown
    Преобразует объекты данных в таблицу формата Markdown
    """
    def build(self, format: str, data: list) -> str:
        """
        Сформировать Markdown таблицу из объектов данных
        Аргументы:
            format (str): Формат ответа
            data (list): Список объектов данных для преобразования
        Возвращает:
            str: Таблица в формате Markdown
        Выбрасывает:
            operation_exception: Если невозможно сформировать таблицу
        """
        text = super().build(format, data)

        try:

            field_names = self._get_field_names(data[0])
            markdown_table = self._build_table_header(field_names)
            markdown_table += self._build_header_separator(field_names)
            markdown_table += self._build_data_rows(data, field_names)
            return markdown_table

        except Exception as error:
            raise operation_exception(f"Ошибка формирования Markdown таблицы: {str(error)}")

    def _get_field_names(self, sample_object) -> list:
        """
        Получить список имен полей объекта
        Аргументы:
            sample_object: Объект для анализа полей
        Возвращает:
            list: Список имен полей
        """
        return common.get_fields(sample_object)

    def _build_table_header(self, field_names: list) -> str:
        """
        Построить строку заголовка таблицы
        Аргументы:
            field_names (list): Список имен полей
        Возвращает:
            str: Строка заголовка в формате Markdown
        """
        header_row = "| " + " | ".join(field_names) + " |\n"
        return header_row

    def _build_header_separator(self, field_names: list) -> str:
        """
        Построить разделитель заголовка таблицы
        Аргументы:
            field_names (list): Список имен полей
        Возвращает:
            str: Строка разделителя в формате Markdown
        """
        separator_cells = ["---"] * len(field_names)
        separator_row = "| " + " | ".join(separator_cells) + " |\n"
        return separator_row

    def _build_data_rows(self, data: list, field_names: list) -> str:
        """
        Построить строки с данными таблицы
        Аргументы:
            data (list): Список объектов данных
            field_names (list): Список имен полей
        Возвращает:
            str: Все строки данных в формате Markdown
        """
        data_rows = ""

        for data_item in data:
            field_values = []
            for field_name in field_names:
                try:
                    field_value = str(getattr(data_item, field_name))
                    field_values.append(field_value)
                except AttributeError:
                    field_values.append("")
            data_row = "| " + " | ".join(field_values) + " |\n"
            data_rows += data_row

        return data_rows