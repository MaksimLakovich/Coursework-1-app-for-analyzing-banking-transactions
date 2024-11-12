import datetime
from pathlib import Path
from typing import Union

import pandas as pd

from logger import get_logger_user_operations

# Инициализируем логгер для utils
logger = get_logger_user_operations(__name__)


def read_data_with_user_operations(path_to_file: Union[str, Path]) -> pd.DataFrame:
    """Функция считывает банковские операции пользователя из Excel-файла и возвращает данные в DataFrame.
    :param path_to_file: Путь к Excel-файлу.
    :return: Данные в формате DataFrame или пустой DataFrame в случае ошибки."""

    try:
        logger.debug("Начато открытие и считывание Excel данных")
        df_user_operations = pd.read_excel(path_to_file)
        logger.debug("DataFrame успешно создан и возвращен для использования в других функциях")
        return df_user_operations

    except FileNotFoundError as e:
        logger.error(f"Файл с excel-файла не найден: {path_to_file}. {e}")

    except pd.errors.EmptyDataError as e:
        logger.error(f"Файл {path_to_file} пустой и не содержит никаких данных. {e}")

    return pd.DataFrame()  # Возвращаем пустой DataFrame, если чтение excel-файла не удалось


def greeting() -> str:
    """Функция возвращает приветствие в зависимости от времени суток.
    :return: Приветствие в формате строки."""

    logger.debug("Определение текущего времени для формирования будущего приветствия")
    current_time = datetime.datetime.now()
    hour_now = current_time.hour

    if 6 <= hour_now < 11:
        logger.info("Определено приветствие как 'Доброе утро'")
        return "Доброе утро"
    elif 11 <= hour_now < 18:
        logger.info("Определено приветствие как 'Добрый день'")
        return "Добрый день"
    elif 18 <= hour_now < 23:
        logger.info("Определено приветствие как 'Добрый вечер'")
        return "Добрый вечер"
    else:
        logger.info("Определено приветствие как 'Доброй ночи'")
        return "Доброй ночи"
