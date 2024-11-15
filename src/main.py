import pandas as pd

from config import excel_file_user_operations
from src.utils import (
    filter_top_transactions,
    get_card_cashback,
    get_cards_info,
    greeting,
    read_data_with_user_operations,
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

    # Получение кешбэка
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
