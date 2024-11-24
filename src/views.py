import json

import pandas as pd

from config import excel_file_user_operations, json_file_user_settings
from logger import get_logger_response_for_main_page
from src.utils import (
    filter_exchange_rates_from_user_settings,
    filter_stock_from_user_settings,
    filter_top_transactions,
    get_card_cashback,
    get_cards_info,
    greeting,
    read_data_with_user_operations,
    read_user_settings_for_exchange_rates_and_stock,
)

# Инициализирую логгер для views
logger = get_logger_response_for_main_page(__name__)


def response_for_main_page(date: str) -> str:
    """Функция для страницы 'Главная' принимает на вход дату. И возвращает данные для вывода на веб-странице с
    начала месяца (на который выпадает входящая дата) по входящую дату.
    :param date: Входящая пользовательская дата для определения диапазона данных.
    :return: JSON-ответ для страницы 'Главная'."""

    # Преобразую входящую дату от пользователя в формат pandas.Timestamp для последующей фильтрации.
    # Создал дату начала и окончания выполняя условие БТ - "Если дата — 20.05.2020, то данные для анализа будут
    # в диапазоне 01.05.2020-20.05.2020"
    logger.debug("Установка даты начала и даты окончания в диапазоне")
    end_date = pd.Timestamp(date)
    start_date = end_date.replace(day=1)

    # Чтение excel-файла и создание DataFrame
    df_all_user_operations = read_data_with_user_operations(path_to_file=excel_file_user_operations)

    # Преобразую столбец "Дата платежа" в datetime
    logger.debug("Преобразование столбца 'Дата платежа' в datetime для последующих операций фильтрации")
    df_all_user_operations["Дата платежа"] = pd.to_datetime(
        df_all_user_operations["Дата платежа"], format="%d.%m.%Y", errors="coerce"
    )

    # Фильтрация полученного DataFrame по сформированному диапазону от start_date до end_date
    logger.debug("Фильтрация полученного DataFrame по сформированному диапазону от start_date до end_date")
    df_filtered_operations = df_all_user_operations.loc[
        (df_all_user_operations["Дата платежа"] >= start_date) & (df_all_user_operations["Дата платежа"] <= end_date)
    ]

    # Приветствие пользователя системы в зависимости от времени суток
    greeting_ = greeting()

    # Получение инфо по каждой карте (последние 4 цифры, общая сумма расходов, кэшбэк)
    # Объединение итогового DataFrame по "Номер карты" данными из card_expenses и card_cashback
    logger.debug("Объединение итогового DataFrame по 'Номер карты' данными из card_expenses и card_cashback")
    cards = pd.merge(
        get_cards_info(df_filtered_operations), get_card_cashback(df_filtered_operations), on="Номер карты", how="left"
    )
    # Преобразование данных карт в список словарей
    logger.debug("Преобразование данных карт в список словарей с переименованием колонок для json-ответа")
    cards_list = cards.rename(
        columns={"Номер карты": "last_digits", "Сумма расходов": "total_spent", "Рассчитанный кэшбэк": "cashback"}
    ).to_dict(orient="records")

    # Получение топ-5 транзакций по сумме платежа
    top_transactions = filter_top_transactions(df_filtered_operations)
    # Преобразование данных топ-5 транзакций в список словарей
    logger.debug("Преобразование данных топ-5 транзакций в список словарей с переименованием колонок для json-ответа")
    top_transactions_list = top_transactions.rename(
        columns={"Дата платежа": "date", "Сумма платежа": "amount", "Категория": "category", "Описание": "description"}
    ).to_dict(orient="records")

    # Преобразую даты в строку чтоб потом корректно работал json.dumps
    logger.debug("Преобразование даты в строку чтоб потом корректно работал json.dumps")
    for transaction in top_transactions_list:
        transaction["date"] = transaction["date"].strftime("%d.%m.%Y")

    # Чтение json-файла с пользовательскими настройками для валют и акций
    user_settings = read_user_settings_for_exchange_rates_and_stock(path_to_file=json_file_user_settings)

    # Запрос по API данных о текущих курс валют, которые указаны в пользовательских настройках
    currency_rates = filter_exchange_rates_from_user_settings(user_settings)

    # Запрос по API данных о стоимости акций из S&P500, которые указаны в пользовательских настройках
    stock_prices = filter_stock_from_user_settings(user_settings)

    logger.info("Формирование итогового ответа в заданном формате")
    response = {
        "greeting": greeting_,
        "cards": cards_list,
        "top_transactions": top_transactions_list,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
    }

    logger.debug("Возврат итогового ответа в json-файле")
    return json.dumps(response, ensure_ascii=False, indent=4)
