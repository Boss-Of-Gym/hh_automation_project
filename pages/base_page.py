from playwright.sync_api import Page, expect, Locator
from urllib.parse import urljoin
# Импортируем настройки, чтобы использовать BASE_URL.

try:
    import sys
    from pathlib import Path
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))
    from config import settings
except ImportError:
     raise ImportError("Не удалось импортировать settings из папки 'config'. Проверьте структуру проекта и путь импорта в base_page.py.")

class BasePage:
    """Базовый класс для всех Page Object'ов."""

    def __init__(self, page: Page):
        """
        Инициализирует BasePage объектом Playwright Page.

        Args:
            page: Объект Playwright Page для взаимодействия.
        """
        self.page = page
        self.base_url = settings.BASE_URL
        self.cookie_accept_button = self.page.locator("[data-qa='cookies-policy-informer-accept']")

    def open(self, url: str = ""):
        """
        Переходит по указанному URL относительно BASE_URL.
        После перехода выполняет общие действия, такие как ожидание загрузки и закрытие куки.

        Args:
            url: Часть URL после BASE_URL (по умолчанию главная страница "").
        """
        full_url = urljoin(self.base_url, url)
        # Переходим на URL. Таймаут навигации установлен в conftest.py.
        self.page.goto(full_url)        
        self.wait_for_page_fully_load() # Ждем полной загрузки страницы
        self.click_accept_cookies() # Закрываем баннер куки, если он есть

    def wait_for_page_fully_load(self, state: str = "load"):
        """
        Ожидает определенного состояния загрузки страницы.

        Args:
            state: Состояние загрузки ('load', 'domcontentloaded', 'networkidle'). По умолчанию 'load'.
        """
        try:
            self.page.wait_for_load_state(state, timeout=settings.PAGE_LOAD_TIMEOUT) # Используем таймаут из settings
        except Exception as e:
             print(f"Предупреждение: Ошибка при ожидании состояния загрузки '{state}': {e}")
             # Не падаем жестко, просто логируем предупреждение, возможно, страница все равно usable

    def click_accept_cookies(self):
        """
        Кликает по кнопке принятия куки, если баннер виден.
        Предполагает, что локатор self.cookie_accept_button определен.
        """
        try:
            expect(self.cookie_accept_button).to_be_visible(timeout=5000) # Проверяем видимость баннера с небольшим таймаутом
            self.cookie_accept_button.click() # Кликаем по кнопке принятия
            expect(self.cookie_accept_button).not_to_be_visible(timeout=5000) # Ожидаем скрытия баннера
            print("Баннер куки закрыт.") # Логирование
        except Exception as e:
            print("Баннер куки не найден или не удалось закрыть.") # Логирование

    # Здесь можно добавить другие общие методы, например:
    # def scroll_to_element(self, locator: Locator): # Пример метода для прокрутки к элементу
    #     locator.scroll_into_view_if_needed()

    # def handle_alert(self, accept: bool = True): # Пример метода для работы с алертами
    #     def dialog_handler(dialog):
    #         if accept:
    #             dialog.accept()
    #         else:
    #             dialog.dismiss()
    #     self.page.once("dialog", dialog_handler)