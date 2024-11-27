import datetime as dt
import functools
import json
from typing import Any, Callable, Optional

import pandas as pd

from config import DATA_DIR
from logger import get_logger_for_reports

# Инициализирую логгер для reports
logger = get_logger_for_reports(__name__)


def save_report(file_name: Optional[str] = None) -> Callable:
    """Декоратор для функций-отчетов, который записывает в файл результаты полученные в функциях-отчеты."""

    def decorator(func: Callable) -> Callable:
        # С помощью библиотеки functools охраняю метаданные оборачиваемой функции, чтоб потом в логгах,
        # при использовании, например {spending_by_category.__name__} записывалось spending_by_category, а не wrapper
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Выполнение функции-отчета
            result = func(*args, **kwargs)
            # Определение имени отчета по умолчанию, если оно не задано в параметре декоратора при его использовании
            default_file = f"report_{dt.datetime.now().strftime("%Y.%m.%d_%H:%M:%S")}.json"
            target_file = file_name if file_name else default_file
            # Преобразование данных для сериализации.
            # Нужно во входящем DataFrame изменить формат "Дата платежа" из формата pandas в строку заданного формата.
            result_dict = result.copy()
            if "Дата платежа" in result_dict.columns:
                result_dict["Дата платежа"] = result_dict["Дата платежа"].dt.strftime("%d.%m.%Y")
            # Сохранение результатов отчета в заданный файл
            with open(f"{DATA_DIR}/{target_file}", "w", encoding="utf-8") as file:
                json.dump(result_dict.to_dict(orient="records"), file, ensure_ascii=False, indent=4)
            return result

        return wrapper

    return decorator


@save_report("report_spending_by_category.json")
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

    logger.debug(f"Возврат результата отчета {spending_by_category.__name__}")
    return df_sorted_transactions
