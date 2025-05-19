import os
from dotenv import load_dotenv
# Загружаем переменные окружения из файла .env
load_dotenv()

""" --- Общие Настройки --- """

BASE_URL = os.getenv("BASE_URL", "https://kaliningrad.hh.ru/") # Базовый URL тестируемого приложения hh.ru.

""" --- Настройки Браузера --- """
# Тип браузера по умолчанию для запуска тестов (chromium, firefox, webkit).
# Читается из переменной окружения BROWSER. По умолчанию - chromium.
DEFAULT_BROWSER = os.getenv("BROWSER", "chromium").lower()
# Режим запуска браузера: True для headless (без UI), False для режима с окном.
# Читается из переменной окружения HEADLESS. По умолчанию - true.
# Значение из переменной окружения должно быть "true" или "false" (без учета регистра).
HEADLESS_MODE = os.getenv("HEADLESS", "true").lower() == "true"
# Замедление выполнения операций Playwright на указанное количество миллисекунд.
# Полезно для наблюдения за выполнением теста. 0 - без замедления.
# Читается из переменной окружения SLOW_MO. По умолчанию - 0.
SLOW_MO = int(os.getenv("SLOW_MO", "0"))

""" --- Настройки Таймаутов (в миллисекундах) --- """
# Таймаут по умолчанию для большинства операций Playwright (ожидание элементов, действия).
# Читается из переменной окружения DEFAULT_TIMEOUT_MS. По умолчанию - 60 секунд (60000 мс).
DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT_MS", "60000"))
# Таймаут для ожидания полной загрузки страницы (событие 'load').
# Читается из переменной окружения PAGE_LOAD_TIMEOUT_MS. По умолчанию - 30 секунд (30000 мс).
PAGE_LOAD_TIMEOUT = int(os.getenv("PAGE_LOAD_TIMEOUT_MS", "60000"))
# Таймаут для ожидания завершения навигации (перехода на новую страницу).
# Читается из переменной окружения NAVIGATION_TIMEOUT_MS. По умолчанию - 30 секунд (30000 мс).
NAVIGATION_TIMEOUT = int(os.getenv("NAVIGATION_TIMEOUT_MS", "60000"))

""" --- Настройки Отчетов --- """
# Директория для сохранения артефактов тестирования (скриншотов, трейсов, HTML-отчетов).
# По умолчанию создается папка 'test_results' в той же директории, где находится файл settings.py.
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_results")

# --- Учетные Данные (Пример - управляйте безопасно!) ---
# Если нужны учетные данные, их также можно читать из переменных окружения
# TEST_USERNAME = os.getenv("TEST_USERNAME")
# TEST_PASSWORD = os.getenv("TEST_PASSWORD")

# --- Информация об Окружении (Опционально, если BASE_URL достаточно) ---
# Можно добавить переменную, просто указывающую на активное тестовое окружение
# ACTIVE_ENVIRONMENT = os.getenv("TEST_ENV", "local").lower()