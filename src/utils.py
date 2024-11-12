from pathlib import Path
from typing import Union

import pandas as pd

from logger import get_logger_user_operations

# Инициализируем логгер для utils
logger_get_user_operations = get_logger_user_operations(__name__)


def read_data_with_user_operations(path_to_file: Union[str, Path]) -> pd.DataFrame:
    """Функция считывает банковские операции пользователя из Excel-файла и возвращает данные в DataFrame.
    :param path_to_file: Путь к Excel-файлу.
    :return: Данные в формате DataFrame или пустой DataFrame в случае ошибки."""

    try:
        logger_get_user_operations.debug("Начато открытие и считывание Excel данных")
        df_user_operations = pd.read_excel(path_to_file)
        logger_get_user_operations.debug("DataFrame успешно создан и возвращен для использования в других функциях")
        return df_user_operations

    except FileNotFoundError as e:
        logger_get_user_operations.error(f"Файл с excel-файла не найден: {path_to_file}. {e}")

    except pd.errors.EmptyDataError as e:
        logger_get_user_operations.error(f"Файл {path_to_file} пустой и не содержит никаких данных. {e}")

    return pd.DataFrame()  # Возвращаем пустой DataFrame, если чтение excel-файла не удалось
