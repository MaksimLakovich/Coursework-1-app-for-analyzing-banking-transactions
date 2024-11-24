from pathlib import Path


# Определение пути к корневой директории проекта, это будет использоваться далее в определении необходимых путей
BASE_DIR = Path(__file__).resolve().parent


# Определение пути к директории куда будут записываться логи приложения (../logs/) и определение имени файла для логов
LOGS_DIR = BASE_DIR / "logs"
log_utils_file = LOGS_DIR / "utils.log"
log_views_file = LOGS_DIR / "views.log"
log_services_file = LOGS_DIR / "services.log"


# Чтобы создать автоматически необходимую директорию (../logs/), если ее не существует еще мы используем эту функцию.
# Которую буду вызывать из main.py, что логично, так как директории обычно инициализируются при запуске приложения.
def initialize_directories() -> None:
    """Функция создает необходимые директории, если они еще не существуют."""

    LOGS_DIR.mkdir(parents=True, exist_ok=True)


# Определение пути к Excel-файлу c БАНКОВСКИМИ ТРАНЗАКЦИЯМИ, который размещается в проекте в директории (../data/)
DATA_DIR = BASE_DIR / "data"
excel_file_user_operations = DATA_DIR / "operations.xlsx"


# Определение пути к JSON-файлу c настройками пользователя, который размещается в проекте в директории (../data/)
DATA_DIR = BASE_DIR / "data"
json_file_user_settings = DATA_DIR / "user_settings.json"
