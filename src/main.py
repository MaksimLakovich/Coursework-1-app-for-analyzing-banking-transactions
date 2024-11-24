from config import excel_file_user_operations
from src.services import get_cashback_analysis_by_category
from src.views import response_for_main_page

if __name__ == "__main__":

    user_date = input(
        "Введите дату для вывода данных по банковским операциям (с 01.mm.yyyy по dd.mm.yyyy), где "
        "dd.mm.yyyy это указанная вами дата: "
    )
    print(response_for_main_page(user_date))

    year, month = input(
        "Введите через `-` год и месяц за который будет проводится анализ категорий повышенного "
        "кэшбэка (например: 2021-08): "
    ).split("-")
    print(get_cashback_analysis_by_category(file=excel_file_user_operations, user_year=year, user_month=month))
