from config import excel_file_user_operations
from src.utils import read_data_with_user_operations, greeting

if __name__ == "__main__":

    # Чтение excel-файла и создание DataFrame
    df_data = read_data_with_user_operations(path_to_file=excel_file_user_operations)
    print(df_data)
    print(df_data.head())

    # Приветствие пользователя системы в зависимости от времени суток
    print(greeting())
