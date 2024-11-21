import logging

from config import initialize_directories, log_utils_file, log_views_file

# Инициализируем необходимые директории (сейчас это только инициализация (../logs/) для логов)
initialize_directories()


def get_logger_user_operations(name: str) -> logging.Logger:
    """Функция создает и возвращает настроенный логгер с заданным именем."""

    logger_get_user_operations = logging.getLogger(name)
    file_handler = logging.FileHandler(log_utils_file, "w")
    file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(funcName)s - %(levelname)s: %(message)s")
    file_handler.setFormatter(file_formatter)
    logger_get_user_operations.addHandler(file_handler)
    logger_get_user_operations.setLevel(logging.DEBUG)

    return logger_get_user_operations


def get_response_for_main_page(name: str) -> logging.Logger:
    """Функция создает и возвращает настроенный логгер с заданным именем."""

    logger_get_response_for_main_page = logging.getLogger(name)
    file_handler = logging.FileHandler(log_views_file, "w")
    file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(funcName)s - %(levelname)s: %(message)s")
    file_handler.setFormatter(file_formatter)
    logger_get_response_for_main_page.addHandler(file_handler)
    logger_get_response_for_main_page.setLevel(logging.DEBUG)

    return logger_get_response_for_main_page
