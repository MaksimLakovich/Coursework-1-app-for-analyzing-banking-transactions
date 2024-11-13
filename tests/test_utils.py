from datetime import datetime
from unittest.mock import MagicMock, patch

import pandas as pd
import pandas.testing as pdt  # Импортирую функцию pd.testing для сравнения 2-х DataFrame (будет вместо assert)
import pytest

from src.utils import greeting, read_data_with_user_operations


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
