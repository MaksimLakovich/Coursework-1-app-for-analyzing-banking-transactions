from config import excel_file_user_operations
from src.reports import spending_by_category
from src.services import get_cashback_analysis_by_category
from src.utils import read_data_with_user_operations
from src.views import response_for_main_page

if __name__ == "__main__":

    # ЗАДАЧА 1
    user_date = input(
        "Введите дату для вывода данных по банковским операциям (с 01.mm.yyyy по dd.mm.yyyy), где "
        "dd.mm.yyyy это указанная вами дата: "
    ).strip()
    print(response_for_main_page(user_date))

    # ЗАДАЧА 2
    year, month = (
        input(
            "Введите через `-` год и месяц за который будет проводится анализ категорий повышенного "
            "кэшбэка (например: 2021-08): "
        )
        .strip()
        .split("-")
    )
    print(get_cashback_analysis_by_category(file=excel_file_user_operations, user_year=year, user_month=month))

    # ЗАДАЧА 3
    transactions = read_data_with_user_operations(path_to_file=excel_file_user_operations)
    user_category = input("Введите название категории: ").strip().lower()
    user_date = input("Введите дату для анализа в формате dd.mm.yyyy: ").strip()
    print(spending_by_category(transactions, user_category, user_date))
