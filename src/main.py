from src.views import response_for_main_page


if __name__ == "__main__":

    user_date = input(
        "Введите дату для вывода данных по банковским операциям (с 01.mm.yyyy по dd.mm.yyyy), где "
        "dd.mm.yyyy это указанная вами дата: "
    )

    print(response_for_main_page(user_date))
