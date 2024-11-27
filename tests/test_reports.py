from unittest.mock import MagicMock, mock_open, patch

import pandas as pd
import pytest

from config import DATA_DIR
from src.reports import save_report, spending_by_category


def test_spending_by_category_successful(fixture_transactions_data: MagicMock) -> None:
    """Тест успешного выполнения spending_by_category."""

    result = spending_by_category(fixture_transactions_data, category="рестораны", date="01.12.2023")
    assert len(result) == 2
    assert result["Категория"].nunique() == 1


def test_spending_by_category_invalid_date(fixture_transactions_data: MagicMock) -> None:
    """Тест обработки некорректной даты."""

    with pytest.raises(ValueError):
        spending_by_category(fixture_transactions_data, category="рестораны", date="invalid_date")


@patch("builtins.open", new_callable=mock_open)
def test_save_report_with_default_file(mock_open_file: MagicMock, fixture_transactions_data: MagicMock) -> None:
    """Тест сохранения отчета с файлом по умолчанию."""

    @save_report()
    def test_function(transactions: pd.DataFrame) -> pd.DataFrame:
        return transactions

    result = test_function(fixture_transactions_data)
    assert result.equals(fixture_transactions_data)
    mock_open_file.assert_called_once()


@patch("builtins.open", new_callable=mock_open)
def test_save_report_with_custom_file(mock_open_file: MagicMock, fixture_transactions_data: MagicMock) -> None:
    """Тест сохранения отчета с указанным названием файла."""

    @save_report(file_name="custom_report.json")
    def test_function(transactions: pd.DataFrame) -> pd.DataFrame:
        return transactions

    result = test_function(fixture_transactions_data)
    assert result.equals(fixture_transactions_data)
    mock_open_file.assert_called_once_with(f"{DATA_DIR}/custom_report.json", "w", encoding="utf-8")
