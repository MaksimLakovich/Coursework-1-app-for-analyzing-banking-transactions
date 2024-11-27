import logging

from config import initialize_directories, log_utils_file, log_views_file, log_services_file, log_reports_file

# Инициализируем необходимые директории (сейчас это только инициализация (../logs/) для логов)
initialize_directories()


def get_logger_user_operations(name: str) -> logging.Logger:
    """Функция создает и возвращает настроенный логгер с заданным именем для модуля utils.py."""

    logger_get_user_operations = logging.getLogger(name)
    file_handler = logging.FileHandler(log_utils_file, "w")
    file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(funcName)s - %(levelname)s: %(message)s")
    file_handler.setFormatter(file_formatter)
    logger_get_user_operations.addHandler(file_handler)
    logger_get_user_operations.setLevel(logging.DEBUG)

    return logger_get_user_operations


def get_logger_response_for_main_page(name: str) -> logging.Logger:
    """Функция создает и возвращает настроенный логгер с заданным именем для модуля views.py."""

    logger_get_response_for_main_page = logging.getLogger(name)
    file_handler = logging.FileHandler(log_views_file, "w")
    file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(funcName)s - %(levelname)s: %(message)s")
    file_handler.setFormatter(file_formatter)
    logger_get_response_for_main_page.addHandler(file_handler)
    logger_get_response_for_main_page.setLevel(logging.DEBUG)

    return logger_get_response_for_main_page


def get_logger_for_services(name: str) -> logging.Logger:
    """Функция создает и возвращает настроенный логгер с заданным именем для модуля services.py."""

    logger_get_services = logging.getLogger(name)
    file_handler = logging.FileHandler(log_services_file, "w")
    file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(funcName)s - %(levelname)s: %(message)s")
    file_handler.setFormatter(file_formatter)
    logger_get_services.addHandler(file_handler)
    logger_get_services.setLevel(logging.DEBUG)

    return logger_get_services


def get_logger_for_reports(name: str) -> logging.Logger:
    """Функция создает и возвращает настроенный логгер с заданным именем для модуля reports.py."""

    logger_get_reports = logging.getLogger(name)
    file_handler = logging.FileHandler(log_reports_file, "w")
    file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(funcName)s - %(levelname)s: %(message)s")
    file_handler.setFormatter(file_formatter)
    logger_get_reports.addHandler(file_handler)
    logger_get_reports.setLevel(logging.DEBUG)

    return logger_get_reports
