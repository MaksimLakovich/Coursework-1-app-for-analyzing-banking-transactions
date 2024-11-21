# Проект 1. Приложение для анализа банковских операций

[1. Цель проекта](#title1) / 
[2. Описание модулей (пакет "src")](#title2) / 
[3. Установка проекта](#title3) / 
[4. Получение ключей для авторизации в API](#title4) / 
[5. Модульное тестирование (пакет "tests")](#title5) / 
[6. Логирование модулей](#title6) / 
[7. Директория проекта "data"](#title7) / 
[8. Описание файла "config.py"](#title8)


### <a id="title1">1. Цель проекта</a>
Реализовать приложение для анализа транзакций, которые находятся в Excel-файле. Приложение будет генерировать JSON-данные для веб-страниц, формировать Excel-отчеты, а также предоставлять другие сервисы.

Полный набор реализуемой в приложении функциональности можно разделить на 3 категории:
- ***Веб-страницы***:
  - Главная
  - События
- ***Сервисы***:
  - Выгодные категории повышенного кешбэка
  - Инвесткопилка
  - Простой поиск
  - Поиск по телефонным номерам
  - Поиск переводов физическим лицам
- ***Отчеты***:
  - Траты по категории
  - Траты по дням недели
  - Траты в рабочий/выходной день

  
### <a id="title2">2. Описание модулей (пакет `src`)</a>

1. Модуль `main.py` содержит код для запуска приложения в целом.


2. Модуль `views.py` содержит главную функцию для веб-страницы "Главная":
   - `response_for_main_page` - функция для страницы "Главная" принимает на вход дату и возвращает данные для вывода на веб-странице с
    начала месяца (на который выпадает входящая дата) по входящую дату.


3. Модуль `utils.py` содержит вспомогательные функции, необходимые для работы функции страницы "Главная":
   - `read_data_with_user_operations()` - данная функция считывает банковские операции пользователя из Excel-файла и возвращает данные в DataFrame для дальнейшего использования в других функциях приложения.
   - `greeting()` - функция возвращает приветствие в зависимости от времени суток.
   - `get_cards_info()` - функция возвращает в формате DataFrame набор данных по каждой карте: последние 4 цифры карты, общая сумма расходов.
   - `get_card_cashback()` - функция возвращает в формате DataFrame данные начисленного кэшбэка по каждой карте.
   - `filter_top_transactions()` - функция возвращает данные топ-5 транзакций по параметру "Сумма платежа". Данные в формате DataFrame с колонками: "Дата платежа", "Сумма платежа", "Категория", "Описание".
   - `read_user_settings_for_exchange_rates_and_stock()` - функция считывает из json-файла настройки пользователя для отображения валют и акций на веб-страницах. Если пользовательских настроек не существует, то возвращаю данные по умолчанию.
   - `filter_exchange_rates_from_user_settings()` - функция принимает данные пользовательских настроек для валют и возвращает текущий курс по ним.
   - `filter_stock_from_user_settings()` - функция принимает данные пользовательских настроек для акций из S&P500 и возвращает их текущий стоимость.


### <a id="title3">3. Установка проекта</a>
1. Клонируйте репозиторий:
```
git clone https://github.com/MaksimLakovich/Coursework-1-app-for-analyzing-banking-transactions.git
```

2. Установите зависимости:
```
poetry install
```


### <a id="title4">4. Получение ключей для авторизации в API</a> 
1. Создайте файл .env в корне проекта из копии подготовленного файла `.env.example`, в котором описаны названия всех переменных, необходимых для работы приложения.
2. Замените значения переменных своими реальными данными.
3. Файл .env должен содержать данные для следующих ресурсов:
   - для конвертации используется Exchange Rates Data API: https://apilayer.com/exchangerates_data-api
     - API_KEY_EXCHANGE_RATES=your_api_key_here.
   - для получения стоимости акций Marketstack API: https://marketstack.com/documentation
     - API_KEY_STOCK_PRICES=your_api_key_here.



### <a id="title5">5. Модульное тестирование (пакет `tests`)</a>
1. Тесты подготовлены отдельными файлами под каждый класс и модуль проекта:
   - `test_utils.py`;
   - `test_views.py`.
2. Для повышения качества тестирования используются фикстуры (файл: `conftest.py`) и параметризация тестов.


### Запуск тестов и анализ покрытия кода:
1. Запустить выполнение тестов необходимо с помощью команды:
```
pytest -v
```
2. Получить анализ покрытия кода тестами можно с помощью команды:
```
pytest --cov=src
```


### <a id="title6">6. Логирование модулей</a>
1. В отдельном модуле `logger.py` реализованы функции, которые создают и возвращают настроенный логгер с заданным именем и параметрами в FileHandler и Formatter для:
   - `get_logger_user_operations()` для модуля `utils.py`;
   - `get_response_for_main_page` для модуля `views.py`.
2. Логи записываются в директорию ***LOGS*** в корне проекта.
Для этого в начале с помощью функции `initialize_directories()` инициализирует все необходимые директории, если их не существует еще. Сейчас это только инициализация `../logs/` для записи логов работы приложения.
3. Формат записи лога в файл включает: метку времени, название модуля, название функции, уровень серьезности и сообщение, описывающее событие или ошибку, которые произошли ***"%(asctime)s - %(name)s - %(funcName)s - %(levelname)s: %(message)s"***.
4. Лог перезаписывается при каждом запуске приложения.


### <a id="title7">7. Директория проекта `data`</a>
Данная директория проекта создана для различных сопутствующих данных необходимых для работы кода, сохранения логов и выполнения тестирования.
1. файл `operations.xls` - пример входящих данных c банковскими транзакциями.
2. файл `user_settings.json` - пример файла в котором сохраняются пользовательские настройки валюты и акции для отображения на веб-страницах:
```json
{
  "user_currencies": ["USD", "EUR"],
  "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
}
```

### <a id="title8">8. Описание файла `config.py`</a>
Для удобства разделения логики и конфигураций, для удобства управления и возможных модификаций использую данный файл конфигурации для хранения путей к файлам и других настроек.
1. Функция `initialize_directories()` - реализована чтобы создавать автоматически нужные директории (например, logs) и которая потом вызывается из main.py. Что логично, поскольку директории обычно инициализируются при запуске приложения.
2. Определен путь к директориям куда будут записываться логи приложения (`../logs/`) и определены имена файлов для логов из модулей:
   - log_utils_file = LOGS_DIR / `utils.log`;
   - log_views_file = LOGS_DIR / `views.log`.
3. Определен путь к Excel-файлу c банковскими операциями `operations.xlsx`, который размещается в директории (`../data/`).
4. Определен путь к пользовательским настройкам отображения информации на веб-страницах `user_settings.json`, которые размещаются в директории (`../data/`).