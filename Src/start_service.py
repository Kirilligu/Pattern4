from Src.reposity import reposity
from Src.Models.range_model import range_model
from Src.Models.group_model import group_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Core.validator import validator, argument_exception, operation_exception
import os
import json
from Src.Models.receipt_model import receipt_model
from Src.Models.receipt_item_model import receipt_item_model
from Src.Dtos.nomenclature_dto import nomenclature_dto
from Src.Dtos.range_dto import range_dto
from Src.Dtos.category_dto import category_dto


class start_service:
    # Репозиторий
    __repo: reposity = reposity()

    # Рецепт по умолчанию
    __default_receipt: receipt_model

    # Словарь который содержит загруженные и инициализованные инстансы нужных объектов
    # Ключ - id записи, значение - abstract_model
    __cache = {}

    # Наименование файла (полный путь)
    __full_file_name: str = ""

    def __init__(self):
        self.__repo.initalize()

    # Singletone
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(start_service, cls).__new__(cls)
        return cls.instance

        # Текущий файл

    @property
    def file_name(self) -> str:
        return self.__full_file_name

    # Полный путь к файлу настроек
    @file_name.setter
    def file_name(self, value: str):
        validator.validate(value, str)
        full_file_name = os.path.abspath(value)
        if os.path.exists(full_file_name):
            self.__full_file_name = full_file_name.strip()
        else:
            raise argument_exception(f'Не найден файл настроек {full_file_name}')

    # Загрузить настройки из Json файла
    def load(self) -> bool:
        if self.__full_file_name == "":
            raise operation_exception("Не найден файл настроек!")

        try:
            with open(self.__full_file_name, 'r', encoding='utf-8') as file_instance:
                settings_data = json.load(file_instance)

                if "default_receipt" in settings_data:
                    receipt_data = settings_data["default_receipt"]
                    return self.convert(receipt_data)

            return False
        except Exception:
            return False

    # Сохранить элемент в репозитории
    def __save_item(self, key: str, dto, item):
        validator.validate(key, str)
        item.unique_code = dto.id
        self.__cache[dto.id] = item
        self.__repo.data[key].append(item)

    # Загрузить единицы измерений
    def __convert_ranges(self, data: dict) -> bool:
        validator.validate(data, dict)
        ranges_list = data.get('ranges', [])
        if len(ranges_list) == 0:
            return False

        for range_data in ranges_list:
            dto = range_dto().create(range_data)
            item = range_model.from_dto(dto, self.__cache)
            self.__save_item(reposity.range_key(), dto, item)

        return True

    # Загрузить группы номенклатуры
    def __convert_groups(self, data: dict) -> bool:
        validator.validate(data, dict)
        categories_list = data.get('categories', [])
        if len(categories_list) == 0:
            return False

        for category_data in categories_list:
            dto = category_dto().create(category_data)
            item = group_model.from_dto(dto, self.__cache)
            self.__save_item(reposity.group_key(), dto, item)

        return True

    # Загрузить номенклатуру
    def __convert_nomenclatures(self, data: dict) -> bool:
        validator.validate(data, dict)
        nomenclatures_list = data.get('nomenclatures', [])
        if len(nomenclatures_list) == 0:
            return False

        for nomenclature_data in nomenclatures_list:
            dto = nomenclature_dto().create(nomenclature_data)
            item = nomenclature_model.from_dto(dto, self.__cache)
            self.__save_item(reposity.nomenclature_key(), dto, item)

        return True

        # Обработать полученный словарь

    def convert(self, data: dict) -> bool:
        validator.validate(data, dict)

        # 1 Созданим рецепт
        cooking_time = data.get('cooking_time', "")
        portions = int(data.get('portions', 0))
        name = data.get('name', "НЕ ИЗВЕСТНО")
        self.__default_receipt = receipt_model.create(name, cooking_time, portions)

        # Загрузим шаги приготовления
        steps_list = data.get('steps', [])
        for step_text in steps_list:
            if step_text.strip() != "":
                self.__default_receipt.steps.append(step_text)

        self.__convert_ranges(data)
        self.__convert_groups(data)
        self.__convert_nomenclatures(data)

        # Собираем рецепт
        compositions_list = data.get('composition', [])
        for composition_data in compositions_list:
            # TODO: Заменить код через Dto
            nomenclature_id = composition_data.get('nomenclature_id', "")
            range_id = composition_data.get('range_id', "")
            value = composition_data.get('value', "")
            nomenclature_item = self.__cache.get(nomenclature_id)
            range_item = self.__cache.get(range_id)
            composition_item = receipt_item_model.create(nomenclature_item, range_item, value)
            self.__default_receipt.composition.append(composition_item)

        # Сохраняем рецепт
        self.__repo.data[reposity.receipt_key()].append(self.__default_receipt)
        return True

    """
    Стартовый набор данных
    """

    @property
    def data(self):
        return self.__repo.data

    """
    Основной метод для генерации эталонных данных
    """

    def start(self):
        current_directory = os.path.dirname(__file__)
        settings_path = os.path.join(current_directory, "settings.json")

        if not os.path.exists(settings_path):
            raise operation_exception(f"Файл настроек не найден: {settings_path}")

        self.file_name = settings_path
        load_result = self.load()

        if not load_result:
            raise operation_exception("Невозможно сформировать стартовый набор данных!")