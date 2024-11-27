from datetime import datetime
from unittest.mock import MagicMock, mock_open, patch

import pandas as pd
import pandas.testing as pdt  # Импортирую функцию pd.testing для сравнения 2-х DataFrame (будет вместо assert)
import pytest

from src.utils import (
    filter_exchange_rates_from_user_settings,
    filter_stock_from_user_settings,
    filter_top_transactions,
    get_card_cashback,
    get_cards_info,
    greeting,
    read_data_with_user_operations,
    read_user_settings_for_exchange_rates_and_stock,
)


@patch("pandas.read_excel")
def test_read_data_with_user_operations_successful(
    mock_read_excel: MagicMock, fixture_dataframe_with_one_operation: pd.DataFrame
) -> None:
    """Тест на успешное чтение EXCEL-файла."""

    # Подготавливаю данные
    mock_test_data = fixture_dataframe_with_one_operation
    # Мокаю возврат mock_read_excel
    mock_read_excel.return_value = mock_test_data
    # Вызываю функцию, которую тестирую
    result = read_data_with_user_operations("some_path_to/operations.xlsx")
    # Проверяю полученный результат эквивалентность с ожидаемым результатом
    expected_result = mock_test_data
    pdt.assert_frame_equal(result, expected_result)  # использую спец.функц. для сравнения 2-х DataFrame вместо assert


@patch("pandas.read_excel")
def test_read_data_with_user_operations_file_not_found(mock_read_excel: MagicMock) -> None:
    """Тест для обработки ошибки при отсутствии файла - FileNotFoundError."""

    # Мокаю возврат ошибки FileNotFoundError
    mock_read_excel.side_effect = FileNotFoundError
    # Вызываю функцию, которую тестирую с несуществующим файлом
    result = read_data_with_user_operations("not_existent_file.xlsx")
    # Проверка, что возвращается пустой DataFrame, как реализовано в функции.
    # Для проверки можно использовать либо pd.testing.assert_frame_equal, либо проверку.empty,
    # если нас интересует только пустота DataFrame
    pdt.assert_frame_equal(result, pd.DataFrame())  # использую спец.функц. для сравнения 2-х DataFrame вместо assert


@patch("pandas.read_excel")
def test_read_data_with_user_operations_empty_file(mock_read_excel: MagicMock) -> None:
    """Тест для обработки ошибки при пустом файле - pd.errors.EmptyDataError."""

    # Мокаю возврат ошибки pd.errors.EmptyDataError
    mock_read_excel.side_effect = pd.errors.EmptyDataError
    # Вызываю функцию, которую тестирую с пустым excel-файлом
    result = read_data_with_user_operations("some_path_to/empty_file.xlsx")
    # Проверка, что возвращается пустой DataFrame, как реализовано в функции.
    # Для проверки можно использовать либо pd.testing.assert_frame_equal, либо проверку.empty,
    # если нас интересует только пустота DataFrame
    pdt.assert_frame_equal(result, pd.DataFrame())  # использую спец.функц. для сравнения 2-х DataFrame вместо assert


@pytest.mark.parametrize(
    "mocked_time, expected_greeting",
    [
        (datetime(2024, 11, 1, 6), "Доброе утро"),
        (datetime(2024, 11, 1, 11), "Добрый день"),
        (datetime(2024, 11, 1, 18), "Добрый вечер"),
        (datetime(2024, 11, 1, 1), "Доброй ночи"),
    ],
)
def test_greeting(mocked_time: MagicMock, expected_greeting: str) -> None:
    """Тест проверки варианта приветствия в зависимости от времени суток."""
    with patch("datetime.datetime") as mock_datetime_datetime:
        mock_datetime_datetime.now.return_value = mocked_time
        assert greeting() == expected_greeting


@pytest.mark.parametrize(
    "expected_data",
    (
        {
            "Номер карты": ["*1234", "*5678"],
            "Сумма расходов": [-1500.0, -200.0],
        },
    ),
)
def test_get_cards_info_successful(fixture_operations_data: pd.DataFrame, expected_data: pd.DataFrame) -> None:
    """Тест для get_cards_info() проверяющий суммирование расходов и группировку по каждой карте."""

    expected_df = pd.DataFrame(expected_data)  # Нельзя в parametrize сразу передать DataFrame (делаю преобразование)
    result = get_cards_info(fixture_operations_data)
    pdt.assert_frame_equal(result, expected_df)


@pytest.mark.parametrize(
    "expected_data",
    (
        {
            "Номер карты": ["*1234", "*5678"],
            "Рассчитанный кэшбэк": [60.0, 2.0],
        },
    ),
)
def test_get_card_cashback_successful(fixture_operations_data: pd.DataFrame, expected_data: pd.DataFrame) -> None:
    """Тест для get_card_cashback() проверяющий расчет кэшбэка по каждой карте."""

    expected_df = pd.DataFrame(expected_data)
    result = get_card_cashback(fixture_operations_data)
    pdt.assert_frame_equal(result, expected_df)


def test_filter_top_transactions_successful(fixture_operations_data: pd.DataFrame) -> None:
    """Тест для filter_top_transactions() с проверкой корректного выбора топ-5 транзакций."""

    expected_data = pd.DataFrame(
        {
            "Дата платежа": pd.to_datetime(["2023-01-01", "2023-01-01", "2023-01-01"]),
            "Сумма платежа": [-1000.0, -500.0, -200.0],
            "Категория": ["Транспорт", "Рестораны", "Супермаркеты"],
            "Описание": ["Поездка", "Ресторан", "Магазин"],
        }
    )

    result = filter_top_transactions(fixture_operations_data)
    pdt.assert_frame_equal(result, expected_data)


@pytest.mark.parametrize(
    "mock_data, expected_settings",
    [
        (
            # Первый параметр (mock_data) — это строка, как бы представляющая на вход содержимое JSON-файла.
            '{"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "AMZN", "GOOGL"]}',
            # Второй параметр (expected_settings) — это ожидаемый результат функции.
            {"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "AMZN", "GOOGL"]},
        ),
        (
            '{"user_currencies": ["GBP"], "user_stocks": ["TSLA", "MSFT"]}',
            {"user_currencies": ["GBP"], "user_stocks": ["TSLA", "MSFT"]},
        ),
    ],
)
def test_read_user_settings_successful(mock_data: MagicMock, expected_settings: dict) -> None:
    """Тест успешного чтения пользовательских настроек из JSON."""

    with patch("builtins.open", mock_open(read_data=mock_data)):
        result = read_user_settings_for_exchange_rates_and_stock("some_path_to/operations.xlsx")
        assert result == expected_settings


def test_read_user_settings_file_not_found() -> None:
    """Тест обработки ситуации, когда JSON-файл не найден и возвращаю данные установленные по умолчанию."""

    with patch("builtins.open", side_effect=FileNotFoundError):
        result = read_user_settings_for_exchange_rates_and_stock("fake_path/user_settings.json")
        expected_settings = {"user_currencies": ["USD"], "user_stocks": ["AAPL", "GOOGL"]}
        assert result == expected_settings


def test_filter_exchange_rates_successful(fixture_user_settings: dict) -> None:
    """Тест успешного получения курсов валют из API."""

    # Определяю результаты для каждой валюты
    mock_responses = [
        {"result": 99.872647},  # Ответ для USD
        {"result": 105.311966},  # Ответ для EUR
    ]
    # Замокать requests.request, чтобы он возвращал заранее определённый результат
    with patch("requests.request") as mock_request:
        # Настраиваю side_effect, чтобы каждый вызов возвращал объект с json()
        mock_request.side_effect = [
            MagicMock(status_code=200, json=MagicMock(return_value=response)) for response in mock_responses
        ]

        result = filter_exchange_rates_from_user_settings(fixture_user_settings)
        expected_result = [
            {"currency": "USD", "rate": 99.872647},
            {"currency": "EUR", "rate": 105.311966},
        ]
        assert result == expected_result


def test_filter_exchange_rates_api_key_not_found(fixture_user_settings: dict) -> None:
    """Тест, проверяющий поведение при отсутствии API ключа."""

    # Патчу os.getenv указывая как бы что он возвращает отсутствие ключа
    with patch("src.utils.os.getenv", return_value=None):
        with pytest.raises(ValueError, match="API_KEY_EXCHANGE_RATES не найден в переменных окружения.env"):
            filter_exchange_rates_from_user_settings(fixture_user_settings)


def test_filter_stock_prices_successful(fixture_user_settings: dict) -> None:
    """Тест успешного получения цены акций по API."""

    # Определяю результаты для каждой акции
    mock_responses = [
        {"data": [{"last": 228.31}]},  # Ответ для AAPL
        {"data": [{"last": 1055.50}]},  # Ответ для AMZN
        {"data": [{"last": 2050}]},  # Ответ для GOOGL
    ]
    # Замокать requests.request, чтобы он возвращал заранее определённый результат
    with patch("requests.get") as mock_get:
        # Настраиваю side_effect, чтобы каждый вызов возвращал объект с json()
        mock_get.side_effect = [
            MagicMock(status_code=200, json=MagicMock(return_value=response)) for response in mock_responses
        ]

        result = filter_stock_from_user_settings(fixture_user_settings)
        expected_result = [
            {"stock": "AAPL", "price": 228.31},
            {"stock": "AMZN", "price": 1055.50},
            {"stock": "GOOGL", "price": 2050},
        ]
        assert result == expected_result


def test_filter_stock_prices_api_key_not_found(fixture_user_settings: dict) -> None:
    """Тест, проверяющий поведение при отсутствии API ключа."""

    # Патчу os.getenv указывая как бы что он возвращает отсутствие ключа
    with patch("src.utils.os.getenv", return_value=None):
        with pytest.raises(ValueError, match="API_KEY_STOCK_PRICES не найден в переменных окружения.env"):
            filter_stock_from_user_settings(fixture_user_settings)
