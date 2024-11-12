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


2. Модуль `views.py` содержит набор функций для страницы "Главная":
   - Функция для страницы "Главная" принимает на вход строку с датой и временем в формате YYYY-MM-DD HH:MM:SS
   - функ.....


2. Модуль `utils.py` содержит вспомогательные функции, необходимые для работы функции страницы "Главная":
   - `read_data_with_user_operations()` - данная функция считывает банковские операции пользователя из Excel-файла и возвращает данные в DataFrame для дальнейшего использования в других функциях приложения.


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


### <a id="title5">5. Модульное тестирование (пакет `tests`)</a>
1. Тесты подготовлены отдельными файлами под каждый класс и модуль проекта:
   - _..........name.py_
2. Для повышения качества тестирования используются фикстуры (файл: conftest.py) и параметризация тестов.


### Запуск тестов и анализ покрытия кода:
1. Запустить выполнение тестов необходимо с помощью команды:
```
pytest -v
```
2. Получить анализ покрытия кода тестами можно с помощью команды:
```
pytest --cov=tests
```


### <a id="title6">6. Логирование модулей</a>
1. В отдельном модуле `logger.py` реализована функция `get_logger_user_operations()`, которая создает и возвращает настроенный логгер с заданным именем и параметрами в FileHandler и Formatter.
2. Логи записываются в директорию ***LOGS*** в корне проекта.
Для этого в начале с помощью функции `initialize_directories()` инициализирует все необходимые директории, если их не существует еще. Сейчас это только инициализация `../logs/` для записи логов работы приложения.
3. Реализована запись логов в файл для следующих модулей проекта:
   - модуль `utils.py`;
   - модуль ....
4. Формат записи лога в файл включает: метку времени, название модуля, название функции, уровень серьезности и сообщение, описывающее событие или ошибку, которые произошли ***"%(asctime)s - %(name)s - %(funcName)s - %(levelname)s: %(message)s"***.
5. Лог перезаписывается при каждом запуске приложения.


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
2. Определен путь к директории куда будут записываться логи приложения (`../logs/`) и определено имя файла для логов.
3. Определен путь к Excel-файлу c банковскими операциями `operations.xlsx`, который размещается в директории (`../data/`).
4. Определен путь к пользовательским настройкам отображения информации на веб-страницах `user_settings.json`, которые размещаются в директории (`../data/`).