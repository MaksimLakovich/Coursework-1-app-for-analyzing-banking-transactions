import json
from unittest.mock import patch, MagicMock

from src.services import get_cashback_analysis_by_category


@patch("src.services.read_data_with_user_operations")
def test_get_cashback_analysis_by_category_successful(
    mock_read_data_with_user_operations: MagicMock, fixture_operations_data: MagicMock
) -> None:
    """Тест успешного выполнения get_cashback_analysis_by_category()."""

    # Мокаю данные операций
    mock_read_data_with_user_operations.return_value = fixture_operations_data

    # Задаю входные параметры
    file_path = "mock_path/operations.xlsx"
    user_year = "2023"
    user_month = "01"

    expected_result = {"Рестораны": 50.0, "Транспорт": 10.0, "Супермаркеты": 2.0}

    result = get_cashback_analysis_by_category(file=file_path, user_year=user_year, user_month=user_month)

    assert json.loads(result) == expected_result
