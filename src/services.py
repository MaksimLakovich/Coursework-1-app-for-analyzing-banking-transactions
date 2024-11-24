import json
from pathlib import Path
from typing import Union

import pandas as pd

from logger import get_logger_for_services
from src.utils import read_data_with_user_operations

# Инициализирую логгер для services
logger = get_logger_for_services(__name__)


def get_cashback_analysis_by_category(file: Union[str, Path], user_year: str, user_month: str) -> str:
    """Функция позволяет проанализировать, какие категории были наиболее выгодными для выбора в качестве категорий
    повышенного кэшбэка.
    :param file: На вход поступает путь к данным с банковскими транзакциями для анализа (data).
    :param user_year: Пользователь устанавливает год (year) за который проводится анализ.
    :param user_month: Пользователь устанавливает месяц (month) за который проводится анализ.
    :return: JSON с анализом, сколько на каждой категории можно заработать кэшбэка в указанном месяце года."""

    logger.debug("Установка фильтрации по году и месяцу")
    # Чтение excel-файла и создание DataFrame
    df_all_user_operations = read_data_with_user_operations(path_to_file=file)

    # Преобразую столбец "Дата платежа" в datetime
    logger.debug("Преобразование столбца 'Дата платежа' в datetime для последующих операций фильтрации")
    df_all_user_operations["Дата платежа"] = pd.to_datetime(
        df_all_user_operations["Дата платежа"], format="%d.%m.%Y", errors="coerce"
    )

    # Фильтрация полученного DataFrame по заданному году и месяцу
    logger.debug("Фильтрация полученного DataFrame по заданному году и месяцу")
    df_filtered_user_operations = df_all_user_operations[
        (df_all_user_operations["Дата платежа"].dt.year == int(user_year))
        & (df_all_user_operations["Дата платежа"].dt.month == int(user_month))
    ]

    # Сортировка успешных расходных операций
    logger.debug("Сортировка успешных расходных операций пользователя")
    sorted_data = df_filtered_user_operations.loc[
        (df_filtered_user_operations["Статус"] == "OK") & (df_filtered_user_operations["Сумма платежа"] < 0)
    ].copy()
    # Добавляю новую колонку "Рассчитанный кэшбэк" и определяю кэшбэк по каждой операции:
    # 1) Если значение есть, то беру его из файла.
    # 2) Если значения нет, считаю 1 рубль на каждые 100 рублей расходов
    logger.debug("Рассчет кэшбэка по каждой операции")
    sorted_data["Рассчитанный кэшбэк"] = sorted_data.apply(
        lambda row: row["Кэшбэк"] if pd.notnull(row["Кэшбэк"]) else abs(row["Сумма платежа"]) // 100, axis=1
    )

    # Группирую по названию категории, суммирую кэшбэк этой категории и в конце сортирую по убыванию
    logger.debug("Группировка и суммирование кэшбэка по каждой категории")
    category_cashback = sorted_data.groupby("Категория")["Рассчитанный кэшбэк"].sum().sort_values(ascending=False)

    logger.info("Формирование итогового ответа в формате json")
    response = category_cashback.to_dict()
    logger.debug("Итоговый ответ успешно сформирован")

    return json.dumps(response, ensure_ascii=False, indent=4)
