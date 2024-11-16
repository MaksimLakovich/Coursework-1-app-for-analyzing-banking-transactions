import pandas as pd

from config import excel_file_user_operations, json_file_user_settings
from src.utils import (
    filter_exchange_rates_from_user_settings,
    filter_top_transactions,
    get_card_cashback,
    get_cards_info,
    greeting,
    read_data_with_user_operations,
    read_user_settings_for_exchange_rates_and_stock,
)

if __name__ == "__main__":

    # Чтение excel-файла и создание DataFrame
    df_user_operations = read_data_with_user_operations(path_to_file=excel_file_user_operations)

    # Приветствие пользователя системы в зависимости от времени суток
    print(greeting())

    # Получение инфо по каждой карте (последние 4 цифры, общая сумма расходов)
    card_expenses = get_cards_info(df_user_operations)
    print(card_expenses)
    print(type(card_expenses))

    # Получение кэшбэка
    card_cashback = get_card_cashback(df_user_operations)
    print(card_cashback)
    print(type(card_cashback))

    # Объединение итогового DataFrame по "Номер карты" данными из card_expenses и card_cashback
    total_card_info = pd.merge(card_expenses, card_cashback, on="Номер карты", how="left")
    print(total_card_info)
    print(type(total_card_info))

    # Получение топ-5 транзакций по сумме платежа
    top_operations = filter_top_transactions(df_user_operations)
    print(top_operations)
    print(type(top_operations))

    # Чтение json-файла с пользовательскими настройками для валют и акций
    user_settings = read_user_settings_for_exchange_rates_and_stock(path_to_file=json_file_user_settings)
    print(user_settings)
    print(type(user_settings))

    # Запрос по API данных о текущих курс валют, которые указаны в пользовательских настройках
    currency_rates = filter_exchange_rates_from_user_settings(user_settings)
    print(currency_rates)
    print(type(currency_rates))
