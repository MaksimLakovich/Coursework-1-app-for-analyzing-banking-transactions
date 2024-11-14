from config import excel_file_user_operations
from src.utils import get_cards_info, greeting, read_data_with_user_operations

if __name__ == "__main__":

    # Чтение excel-файла и создание DataFrame
    df_user_operations = read_data_with_user_operations(path_to_file=excel_file_user_operations)

    # Приветствие пользователя системы в зависимости от времени суток
    print(greeting())

    # Получение инфо по каждой карте (последние 4 цифры, общая сумма расходов)
    total_card_expenses = get_cards_info(df_user_operations)
    print(total_card_expenses)
    print(type(total_card_expenses))

    # # Получение кешбэка
    # total_cashback_on_cards = get_card_cashback(df_user_operations)
    # print(total_cashback_on_cards)
