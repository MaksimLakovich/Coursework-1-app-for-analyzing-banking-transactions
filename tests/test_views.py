import json
from typing import Any, Dict
from unittest.mock import MagicMock, patch

import pandas as pd

from src.views import response_for_main_page


@patch("src.views.read_data_with_user_operations")
@patch("src.views.filter_exchange_rates_from_user_settings")
@patch("src.views.filter_stock_from_user_settings")
@patch("src.views.greeting", return_value="Добрый день")
@patch("src.views.get_cards_info")
@patch("src.views.get_card_cashback")
@patch("src.views.filter_top_transactions")
@patch("src.views.read_user_settings_for_exchange_rates_and_stock")
def test_response_for_main_page_successful(
    mock_read_user_settings: MagicMock,
    mock_filter_top_transactions: MagicMock,
    mock_get_card_cashback: MagicMock,
    mock_get_cards_info: MagicMock,
    mock_greeting: MagicMock,
    mock_filter_stock: MagicMock,
    mock_filter_exchange_rates: MagicMock,
    mock_read_data: MagicMock,
    fixture_simple_operations_data: MagicMock,
    fixture_user_settings: dict,
) -> None:
    """Тест успешного выполнения response_for_main_page()."""

    # Настраиваю все моки
    mock_read_data.return_value = fixture_simple_operations_data
    mock_get_cards_info.return_value = pd.DataFrame(
        {"Номер карты": ["*1234", "*5678"], "Сумма расходов": [-1500.0, -2000.0]}
    )
    mock_get_card_cashback.return_value = pd.DataFrame(
        {"Номер карты": ["*1234", "*5678"], "Рассчитанный кэшбэк": [50.0, 20.0]}
    )
    mock_filter_top_transactions.return_value = pd.DataFrame(
        {
            "Дата платежа": pd.to_datetime(["2021-05-10", "2021-05-01"]),
            "Сумма платежа": [-2000.0, -1500.0],
            "Категория": ["Супермаркеты", "Рестораны"],
            "Описание": ["Магазин", "Обед"],
        }
    )
    mock_read_user_settings.return_value = fixture_user_settings
    mock_filter_exchange_rates.return_value = [
        {"currency": "USD", "rate": 75.0},
        {"currency": "EUR", "rate": 90.0},
    ]
    mock_filter_stock.return_value = [
        {"stock": "AAPL", "price": 150.0},
        {"stock": "AMZN", "price": 3200.0},
        {"stock": "GOOGL", "price": 2200.0},
    ]

    # Вызываю функцию и преобразовываю полученные данные из response_for_main_page с помощью loads() из строк JSON
    # в объект Python для того, чтоб потом сравнить expected_result
    result = response_for_main_page("2021-05-10")
    result_data: Dict[str, Any] = json.loads(result)

    expected_result: Dict[str, Any] = {
        "greeting": "Добрый день",
        "cards": [
            {"last_digits": "*1234", "total_spent": -1500.0, "cashback": 50.0},
            {"last_digits": "*5678", "total_spent": -2000.0, "cashback": 20.0},
        ],
        "top_transactions": [
            {
                "date": "10.05.2021",
                "amount": -2000.0,
                "category": "Супермаркеты",
                "description": "Магазин",
            },
            {
                "date": "01.05.2021",
                "amount": -1500.0,
                "category": "Рестораны",
                "description": "Обед",
            },
        ],
        "currency_rates": [
            {"currency": "USD", "rate": 75.0},
            {"currency": "EUR", "rate": 90.0},
        ],
        "stock_prices": [
            {"stock": "AAPL", "price": 150.0},
            {"stock": "AMZN", "price": 3200.0},
            {"stock": "GOOGL", "price": 2200.0},
        ],
    }

    # Сортировка списков для корректного сравнения (без этого pytest выдает ошибку, так как он почему-то
    # перемешивает при сравнении список stock_prices в result_data и expected_result
    result_data["stock_prices"] = sorted(result_data["stock_prices"], key=lambda x: x["stock"])
    expected_result["stock_prices"] = sorted(expected_result["stock_prices"], key=lambda x: x["stock"])

    assert result_data == expected_result
