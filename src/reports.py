import datetime as dt
from typing import Optional

import pandas as pd

from logger import get_logger_for_reports

# Инициализирую логгер для reports
logger = get_logger_for_reports(__name__)


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Функция для отчета "Траты по категории" для анализа трат пользователя.
    :param transactions: DataFrame с банковскими транзакциями.
    :param category: Название категории для фильтрации банковских транзакций.
    :param date: Опциональная дата, которая определяет диапазон фильтрации.
    :return: DataFrame с тратами по заданной категории за последние три месяца (от переданной даты)."""

    # Преобразую столбец "Дата платежа" в datetime
    logger.debug("Преобразование столбца 'Дата платежа' в datetime для последующих операций фильтрации")
    transactions["Дата платежа"] = pd.to_datetime(transactions["Дата платежа"], format="%d.%m.%Y", errors="coerce")

    # Преобразую входящую дату от пользователя в формат pandas.Timestamp для последующей фильтрации.
    # Создал дату начала и окончания выполняя условие БТ - "Если дата не передана, то берется текущая дата."
    logger.debug("Установка даты начала и даты окончания для диапазона фильтрации")
    if date:
        end_date = pd.Timestamp(date)
    else:
        end_date = pd.Timestamp(dt.datetime.now())
    start_date = end_date - pd.DateOffset(months=3)

    # Фильтрация полученного DataFrame по переданной дате (3 мес от этой даты)
    logger.debug("Фильтрация полученного DataFrame по определенному диапазону")
    df_filtered_transactions = transactions.loc[
        (transactions["Дата платежа"] >= start_date) & (transactions["Дата платежа"] <= end_date)
    ]

    # Сортировка успешных расходных операций по заданной категории
    logger.debug("Сортировка успешных расходных операций пользователя по заданной категории")
    df_sorted_transactions = df_filtered_transactions.loc[
        (df_filtered_transactions["Статус"] == "OK")
        & (df_filtered_transactions["Сумма платежа"] < 0)
        & (df_filtered_transactions["Категория"].str.lower() == category)
    ]

    return df_sorted_transactions
