import pytest, time, re, os
from playwright.sync_api import Page, Locator, expect, Dialog
from urllib.parse import urljoin
from config import settings
from pages.base_page import BasePage # Импортируем базовый класс

class HomePage(BasePage):
    """Page object для Главной страницы HH.ru."""

    def __init__(self, page: Page):
        super().__init__(page) # Вызываем конструктор базового класса
        self.url = "/" # Относительный URL главной страницы

        # --- Локаторы элементов Шапки ---
        self.header = self.page.locator("header") # Контейнер шапки
        self.logo_link = self.page.locator("[data-qa='supernova-logo']") # Логотип
        self.region_selector = self.page.locator("//button[@data-qa='mainmenu_areaSwitcher']/child::span") # Регион
        self.jobseeker_link = self.page.locator('a[data-qa="mainmenu_applicant"]') # Соискателям
        self.employer_link = self.page.locator("[data-qa='mainmenu_employer']") # Работодателям
        self.ready_resume_link = self.page.locator("[data-qa='mainmenu_expertresume']") #Готовое резюме
        self.interview_prep_link = self.page.locator("[data-qa='mainmenu_interviewpractice']") #Репетиция собеседования
        self.career_consult_link = self.page.locator('[data-qa="mainmenu_careerconsult"]') # Карьерная консультация
        self.all_services_link = self.page.locator("[data-qa='mainmenu_applicantServices']") #Все сервисы
        self.create_resume_button = self.page.locator("[data-qa='signup']") # Создать резюме (кнопка)
        self.login_button = self.page.locator("[data-qa='login']") # Войти (кнопка)
        # --- Локаторы модального окна выбора региона ---
        self.city_modal_title = self.page.get_by_text("Найдите ваш город")
        self.popular_city = self.page.get_by_text("Популярные города")
        self.find_string = self.page.get_by_role("textbox", name="Поиск по городам")
        self.button_close = self.page.locator(".magritte-action___JtMQB_4-4-35")
        # --- Локаторы модального окна помощи ---
        self.modal_help = self.page.locator("[data-qa='mainmenu_help']")
        self.help_title = self.page.get_by_text("Нужна помощь?")
        self.help_description = self.page.get_by_text("Можно спросить в поддержке или найти ответ самостоятельно")
        self.dialog_help = self.page.get_by_role("dialog", name="Нужна помощь?")
        self.button_help_close = self.page.get_by_label("Нужна помощь?").get_by_role("button").filter(has_text=re.compile(r"^$"))
        self.questions_and_answers = self.page.locator("a[data-qa='mainmenu_anonHelp']")
        self.write_on_email = self.page.locator('a[data-qa="mainmenu_writeToUs"]')
        self.supprot_chat = self.page.locator('div[data-qa="support-chat-button"]')
        self.telegramm_support = self.page.locator('a[aria-label="TELEGRAM"]')
        # --- Локаторы чат-бота внутри hh.ru ---
        self.chat_widget_root = self.page.locator('[data-qa="chatik-root"]')
        self.chat_iframe_element = self.page.locator(".chatik-integration-iframe")
        self.chat_frame = self.page.frame_locator(".chatik-integration-iframe")
        self.chat_message_textbox = self.chat_frame.locator('[data-qa="chatik-new-message-text"]')
        self.chat_technical_support_text = self.chat_frame.get_by_text("Техническая поддержка")
        self.chat_file_input = self.chat_frame.locator('[data-qa="upload-file-input"]')
        self.chat_upload_button = self.chat_frame.get_by_role("button", name="uploadFileButton")
        self.chat_send_button = self.chat_frame.get_by_role("button", name="Отправить")
        self.chat_history_area = self.chat_frame.locator("#chatik_messages_scroller")
        self.button_for_files = self.chat_frame.locator('[data-qa="uploading-files-modal-send-button"]')
        self.button_chat_close = self.page.locator('[data-qa="chatik-close-chatik"]')
        # --- Локатор подтверждения региона ---
        self.region_ok_button = self.page.get_by_role("button", name="Да, верно")
        # --- Локаторы для основного блока поиска на главной странице ---
        self.main_search_input = self.page.get_by_role("textbox", name="Профессия, должность или компания")
        self.main_search_button = self.page.get_by_role("button", name="Найти")
        self.registration_modal_title = self.page.get_by_text("Зарегистрируйтесь — работодатели смогут найти вас и пригласить на работу")
        self.registration_modal_close_button = self.page.locator(".bloko-modal-close-button")
        # --- Локатор для кнопки фильтрации поиска ---
        self.filter_button = self.page.get_by_role("button", name="Расширенный поиск")
        # >>> Локатор для ссылки/переключателя "Я ищу сотрудника" <<<
        self.looking_for_employee_link = self.page.get_by_role("link", name="Я ищу сотрудника")
        self.employer_heading = self.page.get_by_role("heading", name="Разместите вакансию на hh.ru")
        self.employer_description = self.page.get_by_text("И находите сотрудников среди тех, кто хочет у вас работать. hh.ru — сервис № 1")
        self.post_vacancy_button = self.page.get_by_role("button", name="Разместить вакансию").first
        # >>> Локатор для основного заголовка страницы <<<
        self.main_title = self.page.get_by_role("heading", name="Работа найдётся для каждого")
        # >>> Локаторы для блоков статистических данных <<<
        self.supernova_dashboard_footer = self.page.locator(".supernova-dashboard-footer")
        self.resume_stats_block = self.supernova_dashboard_footer.locator(".supernova-dashboard-stats").filter(has_text="резюме")
        self.vacancies_stats_block = self.supernova_dashboard_footer.locator(".supernova-dashboard-stats").filter(has_text="вакансий")
        self.companies_stats_block = self.supernova_dashboard_footer.locator(".supernova-dashboard-stats").filter(has_text="компаний")
        # >>> Локаторы для кнопок магазинов приложений <<<
        self.app_store_link = self.supernova_dashboard_footer.locator(".supernova-app-button_ios")
        self.google_play_link = self.supernova_dashboard_footer.locator(".supernova-app-button_android")
        self.app_gallery_link = self.supernova_dashboard_footer.locator(".supernova-app-button_huawei")
        # >>> Локаторы для Блока ввода номера телефона <<<
        self.phone_block_title = self.page.getByText("Напишите телефон, чтобы работодатели могли предложить вам работу")
        self.phone_number_input = self.page.getByRole("textbox", name="Номер телефона")
        self.phone_continue_button = self.page.getByRole("button", name="Продолжить")
        # Локатор для всего текста соглашения/политики
        self.phone_agreement_policy_text = self.page.getByText("Нажимая «Продолжить», вы подтверждаете, что полностью принимаете условия Соглашения об оказании услуг по содействию в трудоустройстве (оферта) и ознакомились с политикой конфиденциальности") 
        # Локаторы для самих ссылок внутри текста (для кликов)
        self.phone_agreement_link = self.page.getByRole("link", name="Соглашения об оказании услуг по содействию в трудоустройстве (оферта)")
        self.phone_policy_link = self.page.getByRole("link", name="политикой конфиденциальности")
        # >>> Локаторы для Элементов категорий вакансий <<<
        # Элемент-тоггл "Вакансии дня"
        self.vacancies_of_the_day_item = self.page.locator('[data-qa="vacancy-item-desktop"]')
        # Контейнер раскрывающегося контента для "Вакансии дня
        self.vacancies_of_the_day_revealed_content = self.vacancies_of_the_day_item.locator('+ [data-qa="professions-drop-desktop "]')
        # Элемент-тоггл "Компании дня"
        self.companies_of_the_day_item = self.page.locator('[data-qa="company-item-desktop"]')
         # Контейнер раскрывающегося контента для "Компании дня"
        self.companies_of_the_day_revealed_content = self.companies_of_the_day_item.locator('+ [data-qa="professions-drop-desktop "]')
        # Ссылка "Работа из дома"
        self.work_from_home_link = self.page.get_by_role("link", name="Работа из дома")
        # Элемент-тоггл "Подработка"
        self.part_time_item = self.page.locator('[data-qa="professions-item-desktop"]').filter(has=self.page.locator('.dashboard-tiles-item__title', has_text="Подработка")) # Более точный фильтр по тексту заголовка
        # Контейнер раскрывающегося контента для "Подработка"
        self.part_time_revealed_content = self.part_time_item.locator('+ [data-qa="professions-drop-desktop "]')
        # Элемент-тоггл карточка "Курьер"
        self.courier_item = self.page.locator('[data-qa="professions-item-desktop"]').filter(has=self.page.locator('.dashboard-tiles-item__title', has_text="Курьер"))
        # Контейнер раскрывающегося контента для "Курьер"
        self.courier_revealed_content = self.courier_item.locator('+ [data-qa="professions-drop-desktop "]')
        # Элемент-тоггл карточка "Программист"
        self.programmer_item = self.page.locator('[data-qa="professions-item-desktop"]').filter(has=self.page.locator('.dashboard-tiles-item__title', has_text="Программист"))
        # Контейнер раскрывающегося контента для "Программист"
        self.programmer_revealed_content = self.programmer_item.locator('+ [data-qa="professions-drop-desktop "]')
        # Элемент-тоггл карточка "Менеджер"
        self.manager_item = self.page.locator('[data-qa="professions-item-desktop"]').filter(has=self.page.locator('.dashboard-tiles-item__title', has_text="Менеджер"))
        # Контейнер раскрывающегося контента для "Менеджер"
        self.manager_revealed_content = self.manager_item.locator('+ [data-qa="professions-drop-desktop "]')
        # >>> Локатор для кнопки "Ещё 23 профессии" <<<
        self.show_more_professions_button = self.page.get_by_role("button", name="Ещё 23 профессии")
        self.additional_professions_container_click = self.page.locator("div:nth-child(27) > .bloko-column")
        self.additional_professions_container = self.page.locator("div:nth-child(30) > .dashboard-tiles-item-drop-container-inner")
        # >>> Локатор для баннерной ссылки "Ищите работу эффективнее" <<<
        self.hh_pro_banner_link = self.page.locator('[data-banner-id="355"]').get_by_role('link', name='Ищите работу эффективнее', exact=False)
        # >>> Локатор для статического заголовка "Работа в Калининграде" <<<
        self.work_in_kaliningrad_title = self.page.locator("div").filter(has_text=re.compile(r"^Работа в Калининграде$")).first
        # >>> Локатор для части контейнера списка пунктов "Работа в Калининграде" <<<
        self.work_in_kaliningrad_partial_list_container = self.page.locator(".bloko-columns-wrapper > div > div > div > div > div:nth-child(4)")
         # Статический заголовок для блока
        self.vacancies_of_the_day_kaliningrad_title = self.page.get_by_role("heading", name="Вакансии дня в Калининграде")
        # >>> Локаторы для "Вакансии дня в Калининграде" блок <<<
        self.vacancies_list_container = self.page.locator("div.vacancies-of-the-day")
        self.vacancies_list_item_links = self.vacancies_list_container.locator("a.bloko-link.bloko-link_kind-tertiary")
        # >>> Локаторы для блока "Работа по профессиям в Калининграде" <<<
        # Ссылка заголовка блока
        self.work_in_professions_title_link = self.page.get_by_role("link", name="Работа по профессиям в Калининграде")
        # Контейнер списка ссылок профессий
        self.work_in_professions_list_container = self.page.locator('[data-qa="index__work-in-profession-list"]')
        # Локатор для ВСЕХ отдельных ссылок профессий внутри контейнера
        self.work_in_professions_item_links = self.work_in_professions_list_container.locator('li.multiple-column-list-item > span > a.bloko-link.bloko-link_kind-tertiary')
        # >>> Локаторы для блока "Вакансии в мессенджере" <<<
        self.messenger_title = self.page.get_by_role("heading", name="Вакансии в мессенджере")
        # Ссылки мессенджеров
        self.messenger_vk_link = self.page.get_by_role("link", name="Вконтакте")
        self.messenger_telegram_link = self.page.get_by_role("link", name="Telegram")
        self.messenger_viber_link = self.page.get_by_role("link", name="Viber")
        self.messenger_qr_code_image = self.page.get_by_role("img", name="qr-code-telegram")
        self.messenger_static_text = self.page.get_by_text("Чтобы подключить сервис на телефоне, наведите камеру на QR-код")
        # >>> Локаторы для блока "Новости" <<<
        self.news_title_link = self.page.get_by_role("link", name="Новости")
        self.news_block_container = self.page.locator('div.index-news-box')
        self.news_list_container = self.news_block_container.locator('ul')
        self.news_item_links = self.news_list_container.locator('li.news-box-item > a')
         # >>> Локаторы для блока "Статьи" <<<
        self.articles_title_link = self.page.get_by_role("link", name="Статьи")
        self.articles_block_container = self.page.locator('div.index-news-box.index-news-box_article')
        self.articles_list_container = self.articles_block_container.locator('ul')
        self.articles_item_links = self.articles_list_container.locator('li.news-box-item > a')
        self.articles_site_blog_heading = self.page.get_by_role("heading", name="Блог")
        # >>> Локаторы для блока "Полезное" <<<
        self.useful_title = self.page.get_by_role("heading", name="Полезное")
        self.useful_block_container = self.page.locator('div.index-useful')
        self.useful_list_container = self.useful_block_container.locator('ul')
        self.useful_item_links = self.useful_list_container.locator('li.useful-link > a.bloko-link.bloko-link_kind-tertiary')
        # >>> Локаторы для блока "Работа в других городах" <<<
        self.other_cities_title = self.page.get_by_role("heading", name="Работа в других городах")
        self.other_cities_block_container = self.page.locator('div.work-in-other-cities')
        self.other_cities_list_container = self.other_cities_block_container.locator('ul')
        self.other_cities_item_links = self.other_cities_list_container.locator('li.multiple-column-list-item > span > a.bloko-link.bloko-link_kind-tertiary')

    # --- Методы для взаимодействия (действия) ---

    def open(self):
        """
        Открывает главную страницу.
        Использует метод open() базового класса для навигации и общих действий.
        """
        # Вызываем метод open() базового класса, передавая ему специфический URL-путь главной страницы.
        # BasePage.open() выполнит self.page.goto(self.base_url + self.url),
        # а также ожидания загрузки и обработку куки.
        super().open(self.url)     

    def click_region_ok_button(self):
        """Убирает окно подтверждения региона, чтобы можно было взаимодействовать с кнопкой помощи"""
        self.region_ok_button.click()

    def click_city_modal_close_button(self):
        '''Закрывает модальное окно выбора региона.'''
        self.button_close.click()

    def click_logo(self):
        """Кликает по логотипу HH.ru."""
        self.logo_link.click()

    def click_region_selector(self, city_search_query: str, city_radio_full_name: str):
        """Кликает по элементу выбора региона."""
        self.region_selector.click()
        expect(self.city_modal_title).to_be_visible()
        expect(self.popular_city).to_be_visible()
        expect(self.find_string).to_be_visible()
        self.find_string.fill(city_search_query)
        city_radio_locator = self.page.locator("label").filter(has_text=city_radio_full_name).first
        expect(city_radio_locator).to_be_visible(timeout=15000)
        city_radio_locator.click()

    def click_jobseeker_link(self):
        """Кликает по ссылке 'Соискателям'."""
        self.jobseeker_link.click()

    def click_employer_link(self):
        '''Кликаем по ссылке "Работодателям".'''
        self.employer_link.click()

    def click_ready_resume_link(self):
        '''Кликаем по ссылке "Готовое резюме".'''
        self.ready_resume_link.click()

    def click_dynamic_interview_or_consultation_link(self) -> str:
        """
        Кликает по ссылке 'Репетиция собеседования' или 'Карьерная консультация',
        в зависимости от того, какая видна. Возвращает текст кликнутой ссылки.
        """
        combined_selector_string = "[data-qa='mainmenu_interviewpractice'], [data-qa='mainmenu_careerconsult']"
        expect(self.page.locator(combined_selector_string)).to_be_visible(timeout=30000)
        if self.interview_prep_link.is_visible():
            clicked_link_text = self.interview_prep_link.text_content()
            self.interview_prep_link.click()
            return clicked_link_text
        elif self.career_consult_link.is_visible():
            clicked_link_text = self.career_consult_link.text_content()
            self.career_consult_link.click()
            return clicked_link_text
        else:
            print("Error: Neither interview prep nor career consult link is visible after waiting.")
            return "Error: Link not found"

    def click_all_services_link(self):
        '''Кликаем по ссылке "Все сервисы".'''
        self.all_services_link.click()

    def click_help_link(self):
        """Кликает по ссылке 'Помощь' в шапке и ожидает появления модалки."""
        expect(self.modal_help).to_be_visible()
        self.modal_help.click()
        
    def click_help_modal_questions_link(self):
        """Кликает по ссылке 'Вопросы и ответы' в модальном окне помощи."""
        self.questions_and_answers.click()

    def click_help_modal_email_link(self):
        """Кликает по ссылке 'Написать на почту' в модальном окне помощи."""
        self.write_on_email.click()

    def click_help_modal_telegramm_link(self):
        """Кликает по ссылке 'Телеграмм' в модальном окне помощи."""
        self.telegramm_support.click()

    def click_help_modal_ask_chat_link(self):
        """Кликает по ссылке "Спросить в чате" в модальном окне помощи."""
        self.supprot_chat.click()
        expect(self.chat_widget_root).to_be_visible(timeout=30000)

    def send_message_in_chat_iframe(self, message_text: str):
        """
        Взаимодействует с чат iframe для отправки сообщения и опциональной загрузки файла.
        """
        expect(self.chat_message_textbox).to_be_visible(timeout=15000)
        expect(self.chat_technical_support_text).to_be_visible()
        self.chat_message_textbox.fill(message_text)
        expect(self.chat_send_button).to_be_visible()
        self.chat_send_button.click()
        expect(self.chat_message_textbox).to_be_empty(timeout=15000)
        expect(self.chat_history_area).to_be_visible()

    def send_file_in_chat_iframe(self, file_path: str):
        expect(self.chat_upload_button).to_be_visible(timeout=15000)
        self.chat_file_input.set_input_files(file_path)
        expect(self.button_for_files).to_be_visible(timeout=15000)
        self.button_for_files.click()
        expect(self.button_for_files).not_to_be_visible(timeout=15000)
        filename = os.path.basename(file_path)
        sent_file_name_in_history_locator = self.chat_history_area.locator(f'[data-qa="chat-bubble-filename"]:has-text("{filename}")')
        expect(sent_file_name_in_history_locator).to_be_visible(timeout=20000)
      
    def click_chat_modal_close_button(self):
        """Закрывает модальное окно чата"""
        self.button_chat_close.click()
        expect(self.chat_technical_support_text).not_to_be_visible()

    def click_help_modal_close_button(self):
        """Закрывает модальное окно помощи, кликая по кнопке закрытия."""
        self.button_help_close.click()
        expect(self.help_title).not_to_be_visible()

    def click_create_resume_button(self):
        """Кликает по кнопке 'Создать резюме'."""
        self.create_resume_button.click()

    def click_login_button(self):
        """Кликает по кнопке 'Войти'."""
        self.login_button.click()
    def perform_search(self, search_query: str):
        """Выполняет поиск с использованием основного поля поиска и кнопки на главной странице."""
        expect(self.main_search_input).to_be_visible()
        expect(self.main_search_input).to_be_enabled()
        expect(self.main_search_button).to_be_visible()
        expect(self.main_search_button).to_be_enabled()
        self.main_search_input.fill(search_query)
        self.main_search_button.press("Enter")

    def click_filter_button(self):
        """Кликает по кнопке фильтрации ("Расширенный поиск")."""
        expect(self.filter_button).to_be_visible()
        expect(self.filter_button).to_be_enabled()
        self.filter_button.click()

    def click_looking_for_employee_link(self):
        """
        Кликает по ссылке "Я ищу сотрудника".
        """
        # Проверяем видимость и доступность ссылки перед кликом
        expect(self.looking_for_employee_link).to_be_visible()
        expect(self.looking_for_employee_link).to_be_enabled()
        self.looking_for_employee_link.click()

    def click_app_store_link_and_wait_for_page(self) -> Page:
        """
        Кликает по ссылке "Загрузите в App Store" и ожидает открытия новой страницы (вкладки).
        """
        expect(self.app_store_link).to_be_visible()
        expect(self.app_store_link).to_be_enabled()
        # >>> Используем expect_event для ожидания события 'page' (открытие новой страницы) <<<
        with self.page.context.expect_event('page', timeout=settings.NAVIGATION_TIMEOUT) as event_info:
             self.app_store_link.click()
        # Получаем объект вновь открывшейся страницы из информации о событии
        new_page = event_info.value
        new_page.wait_for_load_state("load", timeout=settings.NAVIGATION_TIMEOUT)
        return new_page
    
    def click_google_play_link_and_wait_for_page(self) -> Page:
        """
        Кликает по ссылке "Доступно в Google Play" и ожидает открытия новой страницы (вкладки).
        """
        expect(self.google_play_link).to_be_visible()
        expect(self.google_play_link).to_be_enabled()
        with self.page.context.expect_event('page', timeout=settings.NAVIGATION_TIMEOUT) as event_info:
             self.google_play_link.click()
        new_page = event_info.value
        new_page.wait_for_load_state("load", timeout=settings.NAVIGATION_TIMEOUT)
        return new_page
    
    def click_app_gallery_link_and_wait_for_page(self) -> Page:
        """
        Кликает по ссылке "Скачайте в AppGallery" и ожидает открытия новой страницы (вкладки).
        """
        expect(self.app_gallery_link).to_be_visible()
        expect(self.app_gallery_link).to_be_enabled()
        browser_context = self.page.context
        with browser_context.expect_event('page', timeout=settings.NAVIGATION_TIMEOUT) as event_info:
             self.app_gallery_link.click() # Выполняем клик по ссылке App Gallery
        new_page = event_info.value
        new_page.wait_for_load_state("load", timeout=settings.NAVIGATION_TIMEOUT)
        return new_page
    
     def fill_phone_number(self, phone: str):
        """Заполняет поле ввода номера телефона."""
        expect(self.phone_number_input).to_be_visible()
        expect(self.phone_number_input).to_be_enabled()
        self.phone_number_input.fill(phone)

    def click_phone_continue_button(self):
        """Кликает по кнопке "Продолжить" в блоке номера телефона."""
        expect(self.phone_continue_button).to_be_visible()
        expect(self.phone_continue_button).to_be_enabled()
        self.phone_continue_button.click()

    def click_phone_agreement_link_and_wait_for_page(self) -> Page:
        """
        Кликает по ссылке "Соглашения об оказании услуг..." и ожидает открытия новой страницы (вкладки).
        """
        expect(self.phone_agreement_link).to_be_visible()
        expect(self.phone_agreement_link).to_be_enabled()
        self.phone_agreement_link.click() 

    def click_phone_policy_link_and_wait_for_page(self) -> Page:
        """
        Кликает по ссылке "политикой конфиденциальности" и ожидает открытия новой страницы (вкладки).
        """
        expect(self.phone_policy_link).to_be_visible()
        expect(self.phone_policy_link).to_be_enabled()
        self.phone_policy_link.click() 

    def click_vacancies_of_the_day_item(self):
        """Кликает по элементу "Вакансии дня" (тоггл контента)."""
        expect(self.vacancies_of_the_day_item).to_be_visible()
        expect(self.vacancies_of_the_day_item).to_be_enabled()
        self.vacancies_of_the_day_item.click()

    def click_companies_of_the_day_item(self):
        """Кликает по элементу "Компании дня" (тоггл контента)."""
        expect(self.companies_of_the_day_item).to_be_visible()
        expect(self.companies_of_the_day_item).to_be_enabled()
        self.companies_of_the_day_item.click()

    def click_work_from_home_link(self):
        """
        Кликает по ссылке "Работа из дома".
        Примечание: При клике может появиться модальное окно регистрации,
        после закрытия которого происходит навигация в том же окне.
        Обработка модалки и ожидание навигации выполняются в тестовом методе.
        """
        expect(self.work_from_home_link).to_be_visible()
        expect(self.work_from_home_link).to_be_enabled()
        self.work_from_home_link.click()

    def click_part_time_item(self):
        """Кликает по элементу "Подработка" (тоггл контента)."""
        expect(self.part_time_item).to_be_visible()
        expect(self.part_time_item).to_be_enabled()
        self.part_time_item.click()
    
    def click_courier_item(self):
        """Кликает по карточке "Курьер" (тоггл контента)."""
        expect(self.courier_item).to_be_visible()
        expect(self.courier_item).to_be_enabled()
        self.courier_item.click()

    def click_programmer_item(self):
        """Кликает по карточке "Программист" (тоггл контента)."""
        expect(self.programmer_item).to_be_visible()
        expect(self.programmer_item).to_be_enabled()
        self.programmer_item.click()

    def click_manager_item(self):
        """Кликает по карточке "Менеджер" (тоггл контента)."""
        expect(self.manager_item).to_be_visible()
        expect(self.manager_item).to_be_enabled()
        self.manager_item.click()

     def click_show_more_professions_button(self):
        """Кликает по кнопке "Ещё 23 профессии" для показа дополнительных карточек."""
        expect(self.show_more_professions_button).to_be_visible()
        expect(self.show_more_professions_button).to_be_enabled()
        self.show_more_professions_button.click()

    def click_hh_pro_banner_link_and_wait_for_page(self) -> Page:
        """
        Кликает по баннерной ссылке "Ищите работу эффективнее" и ожидает открытия новой страницы (вкладки).
        Баннер может загружаться динамически, поэтому таймаут ожидания элемента увеличен.
        """
        # Ждем, пока баннерная ссылка станет видимой и доступной (увеличим таймаут ожидания элемента)
        expect(self.hh_pro_banner_link).to_be_visible(timeout=settings.DEFAULT_TIMEOUT * 2) # Например, 20 секунд или больше
        expect(self.hh_pro_banner_link).to_be_enabled(timeout=settings.DEFAULT_TIMEOUT * 2) # Должна быть кликабельной
        # Используем паттерн ожидания новой страницы, работающий в вашем окружении
        # Эта ссылка открывается в НОВОЙ вкладке.
        with self.page.context.expect_event('page', timeout=settings.NAVIGATION_TIMEOUT) as event_info:
             self.hh_pro_banner_link.click()
        new_page = event_info.value
        return new_page
    
    def click_first_vacancy_list_item_and_wait_for_page(self) -> Page:
        """
        Находит и кликает по ПЕРВОЙ ссылке вакансии в списке "Вакансии дня в Калининграде"
        и ожидает открытия новой страницы (вкладки).
        Этот метод используется для тестирования поведения любой ссылки в списке.
        """
        # Ждем, пока список вакансий станет видимым и содержит хотя бы одну ссылку
        expect(self.vacancies_list_container).to_be_visible(timeout=10000)
        # Проверяем, что в списке есть хотя бы один элемент (ссылка) перед попыткой клика
        expect(self.vacancies_list_item_links).to_have_count(lambda count: count > 0, timeout=10000)
        # Находим ПЕРВУЮ ссылку в списке
        first_item_link = self.vacancies_list_item_links.first
        # Проверяем видимость и доступность этой первой ссылки
        expect(first_item_link).to_be_visible()
        expect(first_item_link).to_be_enabled()
        # Ссылки вакансий открываются в НОВОЙ вкладке. Используем паттерн, работающий в вашем окружении.
        # Для информативности можно попробовать получить текст ссылки перед кликом
        try:
            link_text = first_item_link.text_content().strip()
            print(f"Кликаем по первой ссылке в списке вакансий ('{link_text[:50]}...') и ожидаем новой вкладки...") # Обрезаем длинный текст
        except Exception:
             print("Кликаем по первой ссылке в списке вакансий (не удалось получить текст ссылки) и ожидаем новой вкладки...")
        with self.page.context.expect_event('page', timeout=settings.NAVIGATION_TIMEOUT) as event_info:
             first_item_link.click()
        new_page = event_info.value
        return new_page
    
     def click_work_in_professions_title_link(self):
        """
        Кликает по ссылке заголовка "Работа по профессиям в Калининграде".
        Переход происходит в той же вкладке. Ожидание навигации в тесте.
        """
        expect(self.work_in_professions_title_link).to_be_visible()
        expect(self.work_in_professions_title_link).to_be_enabled()
        self.work_in_professions_title_link.click()

    def click_first_work_in_professions_list_item_and_handle_modal(self, page: Page):
        """
        Находит и кликает по ПЕРВОЙ ссылке профессии в списке "Работа по профессиям в Калининграде",
        обрабатывает модальное окно регистрации, которое появляется после клика,
        и ожидает навигацию в той же вкладке.
        Этот метод используется для тестирования поведения любой ссылки в списке.
        """
        expect(self.work_in_professions_list_container).to_be_visible(timeout=10000)
        expect(self.work_in_professions_item_links).to_have_count(lambda count: count > 0, timeout=10000)
        # Находим ПЕРВУЮ ссылку в списке (объект Locator)
        first_item_link = self.work_in_professions_item_links.first
        # Проверяем видимость и доступность этой первой ссылки
        expect(first_item_link).to_be_visible()
        expect(first_item_link).to_be_enabled()
        # Кликаем по ссылке
        try:
            link_text = first_item_link.text_content().strip()
            print(f"Кликаем по первой ссылке профессии ('{link_text[:50]}...') и ожидаем модальное окно/навигацию...")
        except Exception:
             print("Кликаем по первой ссылке профессии (не удалось получить текст ссылки) и ожидаем модальное окно/навигацию...")
        first_item_link.click()
        # --- Обработка модального окна регистрации, которое появляется ПОСЛЕ клика ---
        # Используем локаторы модалки из HomePage или BasePage.
        # Убедитесь, что home_page.registration_modal_title и home_page.registration_modal_close_button доступны.
        try:
            expect(self.registration_modal_title).to_be_visible(timeout=10000)
            print("Модальное окно регистрации появилось после клика.")
            print("Закрываем модальное окно регистрации...")
            expect(self.registration_modal_close_button).to_be_visible()
            self.registration_modal_close_button.click()
            expect(self.registration_modal_title).not_to_be_visible(timeout=10000)
            print("Модальное окно регистрации закрыто.")
        except Exception:
             print("Предупреждение: Модальное окно регистрации не появилось или не удалось закрыть после клика. Продолжаем ожидание навигации.")

    def click_messenger_vk_link_and_wait_for_page(self) -> Page:
        """
        Кликает по ссылке мессенджера VK и ожидает открытия новой страницы.
        """
        expect(self.messenger_vk_link).to_be_visible()
        expect(self.messenger_vk_link).to_be_enabled()
        # Эта ссылка открывается в НОВОЙ вкладке.
        with self.page.context.expect_event('page', timeout=settings.NAVIGATION_TIMEOUT) as event_info:
             self.messenger_vk_link.click()
        new_page = event_info.value
        return new_page

    def click_messenger_telegram_link_and_wait_for_page(self) -> Page:
        """
        Кликает по ссылке мессенджера Telegram, обрабатывает браузерный диалог
        (нажимает "Отмена"), и ожидает открытия новой страницы (вкладки).
        """
        expect(self.messenger_telegram_link).to_be_visible()
        expect(self.messenger_telegram_link).to_be_enabled()
        # Эта ссылка открывается в НОВОЙ вкладке ПОСЛЕ браузерного диалога.
        # Нам нужно обработать диалог ПЕРЕД кликом по элементу, который его вызывает.
        # Определяем обработчик для события диалога
        # Когда диалог появляется, отклоняем его (кликаем "Отмена").
        # Playwright автоматически находит кнопку "Отмена" или аналогичную при dialog.dismiss().
        def dismiss_dialog(dialog: Dialog):
             print(f"Браузерное окно диалога появилось: {dialog.message}")
             dialog.dismiss() # Кликает "Отмена" или закрывает диалог
        # Регистрируем обработчик до выполнения действия, которое вызывает диалог
        # Используем page.once, так как диалог ожидается только один раз на этот клик.
        self.page.once('dialog', dismiss_dialog)
        # Теперь кликаем по ссылке, которая вызывает диалог и новую страницу
        with self.page.context.expect_event('page', timeout=settings.NAVIGATION_TIMEOUT) as event_info:
             self.messenger_telegram_link.click()
        new_page = event_info.value
        return new_page


    def click_messenger_viber_link_and_wait_for_page(self) -> Page:
        """
        Кликает по ссылке мессенджера Viber и ожидает открытия новой страницы (вкладки).
        Браузерный диалог НЕ ожидается для этой ссылки.
        """
        expect(self.messenger_viber_link).to_be_visible()
        expect(self.messenger_viber_link).to_be_enabled()
        # Эта ссылка открывается в НОВОЙ вкладке.
        with self.page.context.expect_event('page', timeout=settings.NAVIGATION_TIMEOUT) as event_info:
             self.messenger_viber_link.click()
        new_page = event_info.value
        return new_page

    def click_news_title_link(self):
        """
        Кликает по ссылке заголовка "Новости".
        Навигация происходит в той же вкладке. Ожидание навигации в тесте.
        """
        expect(self.news_title_link).to_be_visible()
        expect(self.news_title_link).to_be_enabled()
        self.news_title_link.click()

    def click_first_news_list_item(self):
        """
        Находит и кликает по ПЕРВОЙ ссылке новости в списке "Новости".
        Навигация происходит в той же вкладке. Ожидание навигации в тесте.
        """
        # Ждем, пока список новостей станет видимым и содержит хотя бы одну ссылку
        expect(self.news_list_container).to_be_visible(timeout=10000)
        expect(self.news_item_links).to_have_count(lambda count: count > 0, timeout=10000)
        # Находим ПЕРВУЮ ссылку в списке (объект Locator)
        first_item_link = self.news_item_links.first
        # Проверяем видимость и доступность этой первой ссылки
        expect(first_item_link).to_be_visible()
        expect(first_item_link).to_be_enabled()
        try:
            link_text = first_item_link.text_content().strip()
            print(f"Кликаем по первой ссылке новости ('{link_text[:50]}...') и ожидаем навигацию...")
        except Exception:
             print("Кликаем по первой ссылке новости (не удалось получить текст ссылки) и ожидаем навигацию...")
        first_item_link.click()

    def click_articles_title_link(self):
        """
        Кликает по ссылке заголовка "Статьи".
        Навигация происходит в той же вкладке. Ожидание навигации в тесте.
        """
        expect(self.articles_title_link).to_be_visible()
        expect(self.articles_title_link).to_be_enabled()
        self.articles_title_link.click()
        
    def click_first_useful_list_item(self):
        """
        Находит и кликает по ПЕРВОЙ полезной ссылке в списке "Полезное".
        Навигация происходит в той же вкладке. Ожидание навигации в тесте.
        """
        # Ждем, пока список "Полезное" станет видимым и содержит хотя бы одну ссылку
        expect(self.useful_list_container).to_be_visible(timeout=10000)
        expect(self.useful_item_links).to_have_count(lambda count: count > 0, timeout=10000)
        # Находим ПЕРВУЮ ссылку в списке (объект Locator)
        first_item_link = self.useful_item_links.first
        # Проверяем видимость и доступность этой первой ссылки
        expect(first_item_link).to_be_visible()
        expect(first_item_link).to_be_enabled()
        # Кликаем по ссылке
        try:
            link_text = first_item_link.text_content().strip()
            print(f"Кликаем по первой полезной ссылке ('{link_text[:50]}...') и ожидаем навигацию...")
        except Exception:
             print("Кликаем по первой полезной ссылке (не удалось получить текст ссылки) и ожидаем навигацию...")
        first_item_link.click()
 
    def click_first_other_cities_list_item(self):
        """
        Находит и кликает по ПЕРВОЙ ссылке города в списке "Работа в других городах".
        Навигация происходит в той же вкладке. Ожидание навигации в тесте.
        """
        # Ждем, пока список городов станет видимым и содержит хотя бы одну ссылку
        expect(self.other_cities_list_container).to_be_visible(timeout=10000)
        expect(self.other_cities_item_links).to_have_count(lambda count: count > 0, timeout=10000)
        # Находим ПЕРВУЮ ссылку в списке (объект Locator)
        first_item_link = self.other_cities_item_links.first
        # Проверяем видимость и доступность этой первой ссылки
        expect(first_item_link).to_be_visible()
        expect(first_item_link).to_be_enabled()
        # Кликаем по ссылке
        try:
            link_text = first_item_link.text_content().strip()
            print(f"Кликаем по первой ссылке города ('{link_text[:50]}...') и ожидаем навигацию...") # Print partial text for info
        except Exception:
             print("Кликаем по первой ссылке города (не удалось получить текст ссылки) и ожидаем навигацию...")
        first_item_link.click()
