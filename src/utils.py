import datetime
import json
import os
from pathlib import Path
from typing import Any, Dict, Union

import pandas as pd
import requests
from dotenv import load_dotenv

from logger import get_logger_user_operations

# Инициализирую логгер для utils
logger = get_logger_user_operations(__name__)


def read_data_with_user_operations(path_to_file: Union[str, Path]) -> pd.DataFrame:
    """Функция считывает банковские операции пользователя из Excel-файла и возвращает данные в DataFrame.
    :param path_to_file: Путь к Excel-файлу.
    :return: Данные в формате DataFrame или пустой DataFrame в случае ошибки."""

    try:
        logger.debug("Начато открытие и считывание Excel данных")
        df_user_operations = pd.read_excel(path_to_file)
        logger.debug("DataFrame успешно создан и возвращен для использования в других функциях")
        return df_user_operations

    except FileNotFoundError as e:
        logger.error(f"Файл с excel-файла не найден: {path_to_file}. {e}")

    except pd.errors.EmptyDataError as e:
        logger.error(f"Файл {path_to_file} пустой и не содержит никаких данных. {e}")

    return pd.DataFrame()  # Возвращаем пустой DataFrame, если чтение excel-файла не удалось


def greeting() -> str:
    """Функция возвращает приветствие в зависимости от времени суток.
    :return: Приветствие в формате строки."""

    logger.debug("Определение текущего времени для формирования будущего приветствия")
    current_time = datetime.datetime.now()
    hour_now = current_time.hour

    if 6 <= hour_now < 11:
        logger.info("Определено приветствие как 'Доброе утро'")
        return "Доброе утро"
    elif 11 <= hour_now < 18:
        logger.info("Определено приветствие как 'Добрый день'")
        return "Добрый день"
    elif 18 <= hour_now < 23:
        logger.info("Определено приветствие как 'Добрый вечер'")
        return "Добрый вечер"
    else:
        logger.info("Определено приветствие как 'Доброй ночи'")
        return "Доброй ночи"


def get_cards_info(input_data: pd.DataFrame) -> pd.DataFrame:
    """Функция возвращает набор данных по каждой карте: последние 4 цифры карты, общая сумма расходов.
    :param input_data: Данные в формате DataFrame переданные из функции read_data_with_user_operations().
    :return: Данные в формате DataFrame."""

    # Сразу сортирую данные оставляя только успешные расходные операции
    logger.debug("Сортировка операций пользователя")
    sorted_data = input_data.loc[(input_data["Статус"] == "OK") & (input_data["Сумма платежа"] < 0)].copy()
    # Группирую данные по номерам карт и суммирую расходы по ним.
    # Оставляю индекс в виде столбца (as_index=False), чтобы итогом был DataFrame на выходе.
    # Если этого не сделать, то "groupby" вернет Series, а не DataFrame.
    logger.debug("Группировка и суммирование операций пользователя")
    card_expenses = (
        # dropna=True это исключить значения с NaN (можно явно не прописывать, так как по умолчанию True.
        # Например, ниже в функции get_card_cashback() я это явно уже не указываю (результат тот же).
        sorted_data.groupby(by="Номер карты", sort=True, dropna=True, as_index=False)
        .agg({"Сумма платежа": "sum"})  # Применяю sum к "Сумма платежа", если сделать через agg(), то будет DataFrame
        .rename(columns={"Сумма платежа": "Сумма расходов"})  # Переименовываю колонку для читаемости
    )
    logger.debug("DataFrame успешно создан и возвращен для использования в других функциях")
    return card_expenses


def get_card_cashback(input_data: pd.DataFrame) -> pd.DataFrame:
    """Функция возвращает данные начисленного кэшбэка по каждой карте.
    :param input_data: Данные в формате DataFrame переданные из функции read_data_with_user_operations().
    :return: Данные в формате DataFrame с колонками "Номер карты" и "Кэшбэк"."""

    logger.debug("Сортировка операций пользователя")
    sorted_data = input_data.loc[(input_data["Статус"] == "OK") & (input_data["Сумма платежа"] < 0)].copy()
    # Добавляю новую колонку "Рассчитанный кэшбэк" и определяю кэшбэк по каждой операции:
    # 1) Если значение есть, то деру его из файла.
    # 2) Если значения нет, считаю 1 рубль на каждые 100 рублей расходов
    sorted_data["Рассчитанный кэшбэк"] = sorted_data.apply(
        lambda row: row["Кэшбэк"] if pd.notnull(row["Кэшбэк"]) else abs(row["Сумма платежа"]) // 100, axis=1
    )
    # Группирую по номеру карты и суммирую кэшбэк
    logger.debug("Группировка и суммирование кэшбэка по каждой карте")
    card_cashback = sorted_data.groupby(by="Номер карты", as_index=False).agg({"Рассчитанный кэшбэк": "sum"})
    logger.debug("Кэшбэк успешно рассчитан и возвращен для каждой карты")
    return card_cashback


# # ВАРИАНТ 2 КАК МОЖНО НАПИСАТЬ ФУНКЦИЮ С ПОМОЩЬЮ for index, row in sorted_data.iterrows():
# def get_card_cashback(input_data: pd.DataFrame) -> pd.DataFrame:
#     """Функция возвращает данные начисленного кэшбэка по каждой карте.
#     :param input_data: Данные в формате DataFrame переданные из функции read_data_with_user_operations().
#     :return: Данные в формате DataFrame с колонками "Номер карты" и "Кэшбэк"."""
#
#     # Отбираем успешные расходные операции
#     logger.debug("Сортировка операций пользователя")
#     sorted_data = input_data.loc[(input_data["Статус"] == "OK") & (input_data["Сумма платежа"] < 0)].copy()
#     # Добавляю новую колонку "Рассчитанный кэшбэк" и определяю кэшбэк по каждой операции
#     calculated_cashback = []
#     for index, row in sorted_data.iterrows():
#         # Если в колонке "Кэшбэк" есть значение (не NaN), берем его
#         # проверка на NaN (NaN == NaN возвращает FALSE)
#         # NaN символизирует неизвестное или неопределенное значение. Поскольку значение неопределено, его нельзя
#         # считать эквивалентным чему-либо, даже самому себе.
#         if row["Кэшбэк"] == row["Кэшбэк"]:
#             calculated_cashback.append(row["Кэшбэк"])
#         else:
#             # Если значения нет, считаем 1 рубль на каждые 100 рублей расходов
#             cashback_amount = abs(row["Сумма платежа"]) // 100
#             calculated_cashback.append(cashback_amount)
#     # Добавляю рассчитанный кэшбэк как новый столбец в DataFrame
#     sorted_data["Рассчитанный кэшбэк"] = calculated_cashback
#     # Группирую по номеру карты и суммирую кэшбэк
#     card_cashback = (
#         sorted_data.groupby(by="Номер карты", as_index=False).agg({"Рассчитанный кэшбэк": "sum"})
#     )
#     logger.debug("Кэшбэк успешно рассчитан и возвращен для каждой карты")
#     return card_cashback


def filter_top_transactions(input_data: pd.DataFrame) -> pd.DataFrame:
    """Функция возвращает данные топ-5 транзакций по "Сумма платежа".
    :param input_data: Данные в формате DataFrame переданные из функции read_data_with_user_operations().
    :return: Данные в формате DataFrame с колонками: "Дата платежа", "Сумма платежа", "Категория", "Описание"."""

    logger.debug("Начало фильтрации операций для определения топ-5 транзакций")
    filtered_data = input_data.loc[(input_data["Статус"] == "OK") & (input_data["Сумма платежа"] < 0)].copy()
    sorted_data = filtered_data.sort_values(by="Сумма платежа", axis=0, ascending=True)
    # Фильтрую операции без NaN в "Номер карты"с помощью notnull() и вывожу первые 5 с помощью head()
    top_5_data = sorted_data.loc[sorted_data["Номер карты"].notnull()].head(5)
    logger.debug("Топ-5 транзакций успешно определены и возвращены")
    return top_5_data[["Дата платежа", "Сумма платежа", "Категория", "Описание"]]


def read_user_settings_for_exchange_rates_and_stock(path_to_file: Union[str, Path]) -> Dict[str, Any]:
    """Функция считывает из json-файла настройки пользователя для отображения валют и акций на веб-страницах.
    :param path_to_file: Путь к json-файлу.
    :return: Данные настроек пользователя в формате dict.
    Если пользовательских настроек не существует, то возвращаю данные по умолчанию."""

    try:
        logger.debug("Начато открытие и считывание json-файла с пользовательскими настройками")
        with open(path_to_file) as json_data:
            user_settings: Dict[str, Any] = json.load(json_data)
            logger.debug("Пользовательские настройки считаны и успешно возвращены")
            return user_settings

    except FileNotFoundError as e:
        logger.error(f"Файл с json-данными не найден: {path_to_file}. {e}")

    # Возвращаю данные по умолчанию при отсутствии пользовательских настроек
    logger.debug("Пользовательские настройки отсутствуют (переданы данные считающиеся принятыми по умолчанию)")
    return dict(
        {
            "user_currencies": [
                "USD",
            ],
            "user_stocks": [
                "AAPL",
                "GOOGL",
            ],
        }
    )


def filter_exchange_rates_from_user_settings(user_settings: dict) -> list:
    """Функция принимает данные пользовательских настроек для валют и возвращает текущий курс по ним.
    :param: Перечень валют, которые указаны в пользовательских настройках ("user_currencies").
    :return: Курсы валют по интересующим валютам. Пример: "currency_rates": [{"currency": "USD", "rate": 73.21}]."""

    # Загружаю ключ-api из ".env" через dotenv
    logger.debug("Загрузка API ключа из .env файла")
    load_dotenv()
    api_key = os.getenv("API_KEY_EXCHANGE_RATES")
    if not api_key:
        logger.error("API_KEY_EXCHANGE_RATES не найден в переменных окружения.env")
        raise ValueError("API_KEY_EXCHANGE_RATES не найден в переменных окружения.env")

    # Читаем из user_settings валюты по которым необходимо определить курс:
    logger.debug("Получение списка интересующих валют из пользовательских настроек")
    currencies_list = user_settings.get("user_currencies", [])

    # Формирую запросы к API и собираю результаты
    logger.debug("Начало запросов к API для получения курса валют")
    total_result = []

    for currency in currencies_list:
        try:
            url = "https://api.apilayer.com/exchangerates_data/convert"
            payload = {
                "amount": 1,
                "from": currency,
                "to": "RUB",
            }
            headers = {"apikey": api_key}
            response = requests.request("GET", url, headers=headers, params=payload)
            if response.status_code != 200:
                logger.error(f"Ошибка при запросе для валюты {currency}: {response.text}")
                continue
            response_result = response.json()
            currency_rate = response_result.get("result")
            if currency_rate:
                total_result.append({"currency": currency, "rate": currency_rate})
                logger.debug(f"Получен и добавлен курс для {currency}: {currency_rate}")
            else:
                logger.warning(f"Не удалось получить курс для {currency}: {response_result}")
        except requests.RequestException as e:
            logger.error(f"Ошибка при запросе API для валюты {currency}: {e}")

    logger.debug("Запросы к API завершены")
    return total_result
