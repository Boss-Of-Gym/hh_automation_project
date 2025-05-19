import pytest
from playwright.sync_api import Page, sync_playwright, Error # Импортируем Error для обработки исключений
from pytest import FixtureRequest # Тип для запроса фикстуры
import os
from pathlib import Path # Используем pathlib для удобной работы с путями
import sys

# .parent - путь к папке tests
# .parent - путь к корневой директории
project_root = Path(__file__).parent.parent
# Добавляем корневую директорию проекта в sys.path, чтобы можно было импортировать модули из папок на этом уровне
sys.path.insert(0, str(project_root))
# Теперь импортируем модуль settings из папки config
try:
    from config import settings # Импортируем модуль settings из пакета config
except ImportError:
    raise ImportError("Не удалось импортировать settings из папки 'config'. Проверьте структуру проекта и путь импорта в conftest.py.")

""" --- Фикстуры --- """
# Область видимости 'session' означает, что она вычисляется один раз за весь тестовый прогон.
@pytest.fixture(scope="session")
def browser_config(request: FixtureRequest):
    """Предоставляет конфигурацию запуска браузера."""
    # Получаем значение опции --browser, предоставленной pytest-playwright
    browser_option_value = request.config.getoption("--browser")
    # Получаем значение браузера по умолчанию из настроек
    default_browser_setting = settings.DEFAULT_BROWSER
    if browser_option_value is None or (isinstance(browser_option_value, list) and not browser_option_value):
        browser_type = str(default_browser_setting)
    else:
        browser_type = str(browser_option_value)
    # Получаем другие опции командной строки
    headed = request.config.getoption("--headed")
    slow_mo = request.config.getoption("--slowmo")
    print(f"DEBUG: Значение опции --browser (сырое): {browser_option_value}, тип: {type(browser_option_value)}") # Для отладки
    print(f"DEBUG: Настройка DEFAULT_BROWSER: {default_browser_setting}, тип: {type(default_browser_setting)}") # Для отладки
    print(f"DEBUG: Итоговый тип браузера для запуска: {browser_type}, тип: {type(browser_type)}") # Для отладки
    # Проверка на допустимые типы браузеров
    valid_browsers = ["chromium", "firefox", "webkit"]
    if browser_type not in valid_browsers:
         # В сообщении об ошибке указываем все три значения для диагностики
         pytest.fail(f"Неверный тип браузера. Итоговое значение: '{browser_type}'. Сырое значение опции: {browser_option_value}. Настройка по умолчанию: '{default_browser_setting}'. Допустимые значения: {', '.join(valid_browsers)}")
    return {
        "browser_type": browser_type,
        "headless": not headed, # Если указано --headed=True, то headless = False
        "slow_mo": slow_mo,
    }

# Фикстура, гарантирующая существование директории для сохранения артефактов отчетов
# autouse=True означает, что эта фикстура будет автоматически запущена один раз за тестовую сессию.
@pytest.fixture(scope="session", autouse=True)
def create_output_dir():
    """Гарантирует существование директории для артефактов отчетов."""
    output_path = Path(settings.OUTPUT_DIR)
    try:
        output_path.mkdir(parents=True, exist_ok=True)
        print(f"\nАртефакты отчетов будут сохранены в: {output_path.resolve()}")
    except OSError as e:
         pytest.fail(f"Не удалось создать директорию отчетов {output_path}: {e}")

# Основная фикстура 'page', предоставляющая объект Playwright Page
# Область видимости 'function' означает, что новый браузер, контекст и страница создаются для КАЖДОЙ тестовой функции.
@pytest.fixture(scope="function")
def page(request: FixtureRequest) -> Page:
    """Предоставляет объект Playwright Page для каждой тестовой функции."""
    browser_config_dict = request.getfixturevalue("browser_config") # Получаем конфигурацию браузера
    # Используем контекстный менеджер sync_playwright для гарантии закрытия ресурсов
    with sync_playwright() as p:
        # Запускаем выбранный браузер с настройками
        try:
            browser = p[browser_config_dict["browser_type"]].launch(
                headless=browser_config_dict["headless"],
                slow_mo=browser_config_dict["slow_mo"]
            )
        except Exception as e:
             pytest.fail(f"Не удалось запустить браузер {browser_config_dict['browser_type']}: {e}")
        # Создаем новый контекст браузера (изоляция для каждого теста)
        context = browser.new_context(
            # Опционально: задать размер окна браузера (viewport)
            # viewport={"width": 1280, "height": 720},

            # Здесь можно указать параметры записи ВИДЕО, если нужно:
            # record_video_dir=settings.OUTPUT_DIR if settings.HEADLESS_MODE else None, # Записываем видео только в headless
            # record_video_size={"width": 640, "height": 480}, # Опционально: размер видео
            )
        # Устанавливаем таймауты по умолчанию для контекста
        context.set_default_timeout(settings.DEFAULT_TIMEOUT)
        context.set_default_navigation_timeout(settings.NAVIGATION_TIMEOUT)
        # >>> ДОБАВЛЯЕМ ОТЛАДОЧНЫЕ ПРИНТЫ <<<
        print(f"DEBUG: Установлен Playwright default_timeout: {settings.DEFAULT_TIMEOUT}ms")
        print(f"DEBUG: Установлен Playwright navigation_timeout: {settings.NAVIGATION_TIMEOUT}ms")
        # >>> КОНЕЦ ОТЛАДОЧНЫХ ПРИНТОВ <<<
        # Создаем новую страницу в контексте
        page = context.new_page()
        # Определяем путь и имя файла для сохранения трассировки в конце теста
        test_name = request.node.nodeid.replace("::", "__").replace(".py", "").replace("/", "_")
        trace_path = Path(settings.OUTPUT_DIR) / f"{test_name}-trace.zip"
        # Запускаем запись трассировки с нужными опциями
        # screenshots=True: включать скриншоты в трассировку
        # snapshots=True: включать DOM-снапшоты
        # sources=True: включать исходники
        try:
            context.tracing.start(screenshots=True, snapshots=True, sources=True)
        except Exception as e:
            # Не критичная ошибка, если не удалось начать трассировку
            print(f"\nПредупреждение: Не удалось начать трассировку для теста {test_name}: {e}")
        # Создаем новую страницу в контексте
        page = context.new_page()
        # Передаем объект page тестовой функции
        yield page
        # Получаем результат выполнения тестовой функции ('call') благодаря хуку ниже
        test_failed = request.node.rep_call.failed if hasattr(request.node, 'rep_call') else False
        # Если тест упал, сохраняем скриншот
        if test_failed:
            # Путь для скриншота при падении
            screenshot_path = Path(settings.OUTPUT_DIR) / f"{test_name}-failure.png"
            try:
                 page.screenshot(path=screenshot_path)
                 print(f"\nСкриншот сохранен в: {screenshot_path.resolve()}")
            except Exception as e:
                 print(f"\nНе удалось сохранить скриншот для теста {test_name}: {e}")
        try:
            context.tracing.stop(path=trace_path) # Останавливаем и сохраняем в ранее определенный путь
            # Опционально: удалить файл трассировки, если тест прошел успешно, чтобы не засорять папку
            if not test_failed:
                trace_path.unlink(missing_ok=True) # Удаляем файл, если он существует
            else:
                print(f"Трассировка сохранена в: {trace_path.resolve()}") # Если тест упал, сообщаем, куда сохранили
        except Exception as e:
             print(f"\nПредупреждение: Не удалось остановить или сохранить трассировку для теста {test_name}: {e}")
        # Закрываем страницу и браузер контекст
        # Закрытие контекста автоматически останавливает запись трассировки, если она была запущена без указания path
        # Но явный вызов stop(path=...) лучше для контроля имени файла.
        context.close()
        browser.close()

""" --- Хуки Pytest --- """
# Этот хук нужен, чтобы получить результат выполнения тестовой функции ('call') 
# и прикрепить его к объекту теста (item). Это позволяет проверить результат теста в фикстурах (например, в фикстуре page для сохранения артефактов при падении).
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Выполняем все другие хуки для получения объекта отчета (report)
    outcome = yield
    rep = outcome.get_result()
    # Сохраняем объект отчета на элементе теста, используя имя этапа ('setup', 'call', 'teardown')
    setattr(item, "rep_" + rep.when, rep)
# Чтобы проверить, упал ли тест в основной фазе выполнения, мы проверяем request.node.rep_call.failed в фикстуре page.