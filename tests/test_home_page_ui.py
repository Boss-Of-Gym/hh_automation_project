import sys
import os
# Получаем путь к директории, в которой находится текущий файл (tests/)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Получаем путь к родительской директории (корню проекта hh_automation_project/)
project_root = os.path.join(current_dir, os.pardir)
# Добавляем корень проекта в sys.path, если его там еще нет
if project_root not in sys.path:
    sys.path.insert(0, project_root) # Вставляем в начало, чтобы он искался первым
print("Обновленный sys.path:", sys.path) # Проверим, добавился ли путь

import pytest, re
from playwright.sync_api import Page, expect, Dialog # expect для более читаемых проверок ожидания
from pages.home_page import HomePage
from config.settings import BASE_URL
from urllib.parse import urlparse, parse_qs

# Фикстура 'page' предоставляется pytest-playwright автоматически
class TestHomePageHeader:
    """Группа тестов для проверки шапки сайта hh.ru"""
    
    @pytest.mark.skip
    def test_home_page_loads_successfully(self, page: Page):
        """Проверка успешной загрузки главной страницы и заголовка."""
        home_page = HomePage(page)
        home_page.open()
        expect(page).to_have_url(f"{BASE_URL}")
        expect(page).to_have_title("Работа в Калининграде, поиск персонала и публикация вакансий - kaliningrad.hh.ru")
    
    @pytest.mark.skip
    def test_login_button(self, page: Page):
        """Проверка кликабельности кнопки "Войти"."""
        home_page = HomePage(page)
        home_page.open()
        expect(home_page.login_button).to_have_text("Войти")
        home_page.click_login_button()
        expect(page).to_have_url(f"{BASE_URL}account/login?role=applicant&backurl=%2F&hhtmFrom=main") # URL после клика "Войти"
    
    @pytest.mark.skip
    def test_logo_button(self, page: Page):
        home_page = HomePage(page)
        home_page.open()
        home_page.click_region_ok_button()
        expect(home_page.logo_link).to_be_visible()
        home_page.click_logo()
        expect(page).to_have_url(f"{BASE_URL}?hhtmFrom=main")
    
    @pytest.mark.skip
    def test_visible_button_region_and_switch_region(self, page: Page):
        home_page = HomePage(page)
        home_page.open()
        expect(home_page.region_selector).to_be_visible()
        city_search_query = "Мурманск"
        city_radio_full_name = "МурманскРоссия, Мурманская область"
        expected_url_after_change = "https://murmansk.hh.ru/?customDomain=1"
        home_page.click_region_selector(city_search_query, city_radio_full_name)
        expect(home_page.city_modal_title).not_to_be_visible()
        expect(page).to_have_url(expected_url_after_change)
        expect(home_page.region_selector).to_have_text(city_search_query)

    @pytest.mark.skip
    def test_employer_and_jobseeker_button(self, page: Page):
        home_page = HomePage(page)
        home_page.open()
        expect(home_page.employer_link).to_be_visible()
        home_page.click_employer_link()
        expect(page).to_have_url(f"{BASE_URL}employer?hhtmFrom=main") # URL после клика "Работодателям"
        expect(home_page.jobseeker_link).to_have_text("Соискателям")
        home_page.click_jobseeker_link()
        expect(page).to_have_url(f"{BASE_URL}") # URL после клика "Соискателям"
    
    @pytest.mark.skip
    def test_ready_resume_button(self, page: Page):
        home_page = HomePage(page)
        home_page.open()
        expect(home_page.ready_resume_link).to_be_visible()
        home_page.click_ready_resume_link()
        expect(page).to_have_url(f"{BASE_URL}mentors?purposeId=1")

    @pytest.mark.skip
    def test_dynamic_interview_or_consultation_button(self, page: Page):
        home_page = HomePage(page)
        home_page.open()
        is_interview_visible = home_page.interview_prep_link.is_visible()
        is_consultation_visible = home_page.career_consult_link.is_visible()
        assert (is_interview_visible or is_consultation_visible) and (is_interview_visible != is_consultation_visible), \
               "Ошибка: Должна быть видна ровно одна из ссылок 'Репетиция собеседования' или 'Карьерная консультация'."
        expected_url_after_click = None
        if is_interview_visible:
            # Если видна ссылка "Репетиция собеседования"
            expected_url_after_click = f"{BASE_URL}mentors?hhtmFrom=main&hhtmFromLabel=header&purposeId=6"
        elif is_consultation_visible:
             # Если видна ссылка "Карьерная консультация"
             expected_url_after_click = f"{BASE_URL}mentors?hhtmFrom=main&hhtmFromLabel=header&purposeId=2"
        home_page.click_dynamic_interview_or_consultation_link()
        expect(page).to_have_url(expected_url_after_click)

    @pytest.mark.skip
    def test_all_servises_button(self, page: Page):
        home_page = HomePage(page)
        home_page.open()
        expect(home_page.all_services_link).to_be_visible()
        home_page.click_all_services_link()
        expect(page).to_have_url(f"{BASE_URL}services?hhtmFrom=main")

    @pytest.mark.skip
    def test_help_modal_ui_elements_visible_and_text(self, page: Page):
        """Проверяет видимость и текст всех основных элементов в модальном окне 'Помощь'."""
        home_page = HomePage(page)
        home_page.open()
        home_page.click_region_ok_button()
        home_page.click_help_link()
        # Проверяем видимость и текст заголовка
        expect(home_page.help_title).to_be_visible()
        expect(home_page.help_title).to_have_text("Нужна помощь?")
        # Проверяем видимость и текст подзаголовка
        expect(home_page.help_description).to_be_visible()
        expect(home_page.help_description).to_contain_text("Можно спросить в поддержке или найти ответ самостоятельно")
        # Проверяем видимость и текст интерактивных элементов
        expect(home_page.questions_and_answers).to_be_visible()
        expect(home_page.questions_and_answers).to_contain_text("Вопросы и ответы")
        expect(home_page.questions_and_answers).to_be_enabled()
        expect(home_page.write_on_email).to_be_visible()
        expect(home_page.write_on_email).to_contain_text("Написать на почту")
        expect(home_page.write_on_email).to_be_enabled()
        expect(home_page.supprot_chat).to_be_visible()
        expect(home_page.supprot_chat).to_contain_text("Спросить в чате")
        expect(home_page.supprot_chat).to_contain_text("Связаться")
        expect(home_page.supprot_chat).to_be_enabled()
        expect(home_page.telegramm_support).to_be_visible()
        expect(home_page.telegramm_support).to_be_enabled()
        # Проверяем видимость кнопки закрытия модалки
        expect(home_page.button_help_close).to_be_visible()
        expect(home_page.button_help_close).to_be_enabled()
        # Закрываем модалку в конце теста проверки UI
        home_page.click_help_modal_close_button()

    @pytest.mark.skip
    def test_help_modal_questions_link_redirects(self, page: Page):
        """Проверяет перенаправление ссылки 'Вопросы и ответы' в модальном окне помощи."""
        home_page = HomePage(page)
        home_page.open()
        home_page.click_region_ok_button()
        home_page.click_help_link()
        with page.context.expect_page() as new_page_event:
            home_page.click_help_modal_questions_link()
        new_page = new_page_event.value
        # Проверяем ожидаемый URL после клика
        expected_new_window_url = "https://feedback.hh.ru/?category=applicant&utm_source=hh.ru&utm_medium=referral&utm_campaign=from_header_new"
        expect(new_page).to_have_url(expected_new_window_url)
        expect(new_page).to_have_title("База знаний hh.ru — Инструкции и советы по работе на платформе")
        new_page.close()
        expect(home_page.help_title).to_be_visible()
        home_page.click_help_modal_close_button()

    @pytest.mark.skip
    def test_help_modal_email_link_action(self, page: Page):
        """Проверяет действие/перенаправление ссылки 'Написать на почту' в модальном окне помощи."""
        home_page = HomePage(page)
        home_page.open()
        home_page.click_region_ok_button()
        home_page.click_help_link()
        with page.context.expect_page() as new_page_event:
            home_page.click_help_modal_email_link()
        new_page = new_page_event.value
        url_login_and_path = r"account/login?backurl=%2Foauth%2Fauthorize%3Fclient_id%3DIVJ6TLHHP7JRAU3BBJQTPQ0UP3IM6OHNBEK5KV8VAMHHQNSDTLCU3BSASEMMJJ4E%26state%3Dhttps%253A%252F%252Ffeedback.hh.ru%252Fticket%252Fadd%26redirect_uri%3Dhttps%253A%252F%252Ffeedback.hh.ru%252Foauth%252Fauth-redirect%26response_type%3Dcode%26skip_choose_account%3Dtrue&response_type=code&oauth=true"
        expected_new_window_url = f'{BASE_URL}{url_login_and_path}'
        expect(new_page).to_have_url(expected_new_window_url)
        expect(new_page).to_have_title("Вход в личный кабинет")
        new_page.close()
        expect(home_page.help_title).to_be_visible()
        home_page.click_help_modal_close_button()

    @pytest.mark.skip
    def test_help_modal_telegramm_link_prompt(self, page: Page):
        """Проверка, что клик по 'Спросить в чате' в модалке помощи ведет к окну Telegram и обрабатывается диалог."""
        home_page = HomePage(page)
        home_page.open()
        home_page.click_region_ok_button()
        home_page.click_help_link()
        dialog_handled = False
        def dialog_handler(dialog):
            nonlocal dialog_handled
            print(f"Обнаружен диалог типа: {dialog.type}")
            print(f"Текст диалога: {dialog.message}")
            dialog.dismiss()
            dialog_handled = True
        page.on("dialog", dialog_handler)
        # --- Выполнение действия, вызывающего диалог ---
        with page.context.expect_page() as new_page_event:
            home_page.click_help_modal_telegramm_link()
        new_page = new_page_event.value
        expected_new_window_url = "https://telegram.me/hh_applicant_bot"
        expect(new_page).to_have_url(expected_new_window_url)
        new_page.close()
        expect(home_page.help_title).to_be_visible()
        home_page.click_help_modal_close_button()

    @pytest.mark.skip
    def test_help_modal_ask_chat_link_prompt(self, page: Page):
        home_page = HomePage(page)
        home_page.open()
        home_page.click_region_ok_button()
        home_page.click_help_link()
        expect(home_page.supprot_chat).to_be_visible()
        expect(home_page.supprot_chat).to_be_enabled()
        home_page.click_help_modal_ask_chat_link()
        expect(home_page.chat_iframe_element).to_be_visible(timeout=15000)
        # page.pause()
        test_file_path = r"C:\Users\alien\OneDrive\Документы\Code_for_autotest\hh_automation_project\tests\output.txt"
        if os.path.exists(test_file_path):
             home_page.send_file_in_chat_iframe(test_file_path)
        else:
             print(f"Предупреждение: Файл не найден по пути {test_file_path}. Пропуск отправки файла.")
        message_text = "Автоматизированное тестовое сообщение из Playwright."
        home_page.send_message_in_chat_iframe(message_text)
        home_page.click_chat_modal_close_button()
            
    @pytest.mark.skip
    def test_create_resume_button(self, page: Page):
        home_page = HomePage(page)
        home_page.open()
        expect(home_page.create_resume_button).to_be_visible()
        home_page.click_create_resume_button()
        expect(page).to_have_url(f"{BASE_URL}account/signup?backurl=%2Fapplicant%2Fresumes%2Fnew&hhtmFrom=main&hhtmFromLabel=header")

    @pytest.mark.skip
    def test_successful_search_by_keyword(self, page: Page):
        home_page = HomePage(page)
        home_page.open()
        home_page.click_region_ok_button()
        search_query = "Тестировщик"
        home_page.perform_search(search_query)
        expect(home_page.registration_modal_title).to_contain_text("Зарегистрируйтесь — работодатели смогут найти вас и пригласить на работу")
        home_page.registration_modal_close_button.click()
        try:
            expect(home_page.registration_modal_title).not_to_be_visible(timeout=10000)
            print("Модальное окно регистрации подтверждено как закрытое.")
        except Exception as e:
             print(f"Ошибка: Модальное окно регистрации все еще видимо или снова появилось после ожидания перед поиском: {e}")
             pass
        #page.pause()
        current_url = page.url
        parsed_url = urlparse(current_url)
        # Определяем список допустимых путей.
        # path 1: стандартный путь страницы результатов поиска
        # path 2: путь, который может использоваться для прямого показа результатов по запросу (с учетом ТРАНСЛИТЕРАЦИИ запроса в пути)
        # Мы знаем, что "Тестировщик" транслитерируется в "testirovshik".
        expected_paths = [
            "/search/vacancy",
            "/vacancies/testirovshik" # Если бы запросов было много, пришлось бы использовать библиотеку для транслитерации.
        ]
        # Проверяем, что фактический путь URL содержится в списке допустимых путей
        assert parsed_url.path in expected_paths, \
            f"Ожидался путь из {expected_paths} в URL после поиска, но получен '{parsed_url.path}'. Полный URL: {current_url}"
        # --- Проверка параметров запроса (актуально только для стандартного пути) ---
        if parsed_url.path == "/search/vacancy":
            query_params = parse_qs(parsed_url.query)
            assert "text" in query_params, \
                f"В URL результатов поиска '{current_url}' отсутствует параметр 'text' или он пустой."
            # Здесь в параметре запроса text должен быть оригинальный (возможно, URL-кодированный) запрос
            # Проверяем, что оригинальный запрос присутствует в значениях параметра 'text'
            assert search_query in query_params.get("text", []), \
                f"Ожидался параметр 'text' содержащий '{search_query}' в URL '{current_url}', но получены значения: {query_params.get('text')}"

    @pytest.mark.skip
    def test_filter_button_click(self, page: Page):
        """
        Проверяет видимость и кликабельность кнопки "Расширенный поиск"
        и что клик по ней приводит к появлению формы или модального окна фильтров.
        """
        home_page = HomePage(page)
        home_page.open() 
        try:
            home_page.click_region_ok_button()
            print("Модальное окно подтверждения региона закрыто.")
        except Exception:
             print("Предупреждение: Модалка региона не появилась или не удалось закрыть.")
             pass
        try:
            expect(home_page.registration_modal_title).not_to_be_visible(timeout=10000)
            print("Модальное окно регистрации подтверждено как закрытое.")
        except Exception:
             print("Предупреждение: Модальное окно регистрации все еще видимо или снова появилось после ожидания.")
             pass
        home_page.click_filter_button()
        # --- Проверка результата: Верификация того, что появляется после клика ---
        # Ожидаемый URL страницы расширенного поиска
        # >>> Ассерты: Проверяем URL и заголовок на новой странице <<<
        # 1. Проверяем, что текущий URL совпадает с ожидаемым URL страницы расширенного поиска
        # expected_advanced_search_url = f"{home_page.base_url}search/vacancy/advanced?hhtmFrom=main"
        # expect(page).to_have_url(expected_advanced_search_url)
        current_url = page.url
        parsed_url = urlparse(current_url)
        assert parsed_url.path == "/search/vacancy/advanced"
        query_params = parse_qs(parsed_url.query)
        assert query_params.get('hhtmFrom') == ['main']
        # 2. Проверяем, что заголовок "Поиск вакансий" видим на новой странице.
        advanced_search_heading = page.get_by_role("heading", name="Поиск вакансий")
        expect(advanced_search_heading).to_be_visible()
        print("Кнопка фильтрации кликнута. Проверка перехода на страницу расширенного поиска и видимости заголовка выполнена.")

    @pytest.mark.skip
    def test_looking_for_employee_link_click(self, page: Page):
        """
        Проверяет видимость и кликабельность ссылки "Я ищу сотрудника"
        и что клик по ней перенаправляет на страницу для работодателей
        с ожидаемыми элементами.
        """
        home_page = HomePage(page)
        home_page.open()
        try:
            home_page.click_region_ok_button()
            print("Модальное окно подтверждения региона закрыто.")
        except Exception:
             print("Предупреждение: Модалка региона не появилась или не удалось закрыть.")
             pass
        try:
            expect(home_page.registration_modal_title).not_to_be_visible(timeout=10000)
            print("Модальное окно регистрации подтверждено как закрытое.")
        except Exception:
             print("Предупреждение: Модальное окно регистрации все еще видимо или снова появилось после ожидания.")
             pass
        home_page.click_looking_for_employee_link()
        # --- Проверка результата: Верификация навигации на страницу работодателей ---
        # Клик должен привести к навигации на страницу работодателей.
        # Ожидаемый URL страницы работодателей.
        expected_employer_url = f"{home_page.base_url}employer?hhtmFrom=main"
        # 1. Проверяем, что текущий URL совпадает с ожидаемым URL страницы работодателей
        expect(page).to_have_url(expected_employer_url)
        # >>> Ассерты: Проверяем наличие ключевых элементов на странице работодателей <<<
        # 2. Проверяем видимость этих элементов
        expect(home_page.employer_heading).to_be_visible()
        expect(home_page.employer_description).to_be_visible()
        expect(home_page.post_vacancy_button).to_be_visible()
        expect(home_page.post_vacancy_button).to_be_enabled()
        print("Ссылка 'Я ищу сотрудника' кликнута. Проверка перехода на страницу работодателей и видимости ключевых элементов выполнена.")

    @pytest.mark.skip
    def test_main_title_presence_and_text(self, page: Page):
        """
        Проверяет видимость и корректный текст
        основного заголовка на главной странице.
        """
        home_page = HomePage(page)
        home_page.open()
        try:
            home_page.click_region_ok_button()
            print("Модальное окно подтверждения региона закрыто.")
        except Exception:
             print("Предупреждение: Модалка региона не появилась или не удалось закрыть.")
             pass
        try:
            expect(home_page.registration_modal_title).not_to_be_visible(timeout=10000)
            print("Модальное окно регистрации подтверждено как закрытое.")
        except Exception:
             print("Предупреждение: Модальное окно регистрации все еще видимо или снова появилось после ожидания.")
             pass
        # >>> Ассерты: Проверка основного заголовка <<<
        # 1. Проверяем, что заголовок видим
        expect(home_page.main_title).to_be_visible()
        # 2. Проверяем, что текст заголовка совпадает с ожидаемым
        expected_title_text = "Работа найдётся для каждого"
        expect(home_page.main_title).to_have_text(expected_title_text)
        print(f"Тест: Основной заголовок '{expected_title_text}' видим и имеет корректный текст.")

    @pytest.mark.skip
    def test_statistical_numbers_presence_and_values(self, page: Page):
        """
        Проверяет видимость блоков статистических данных (резюме, вакансий, компаний)
        и извлекает их значения.
        """
        home_page = HomePage(page)
        home_page.open()
        try:
            home_page.click_region_ok_button()
            print("Модальное окно подтверждения региона закрыто.")
        except Exception:
             print("Предупреждение: Модалка региона не появилась или не удалось закрыть.")
             pass
        try:
            expect(home_page.registration_modal_title).not_to_be_visible(timeout=10000)
            print("Модальное окно регистрации подтверждено как закрытое.")
        except Exception:
             print("Предупреждение: Модальное окно регистрации все еще видимо или снова появилось после ожидания.")
             pass
        # >>> Ассерты и извлечение данных: Проверка статистических блоков <<<
        print("Проверка видимости блоков статистических данных...")
        expect(home_page.resume_stats_block).to_be_visible(timeout=20000)
        expect(home_page.vacancies_stats_block).to_be_visible(timeout=20000)
        expect(home_page.companies_stats_block).to_be_visible(timeout=20000)
        print("Все блоки статистики видимы.")
        # 2. Извлекаем полный текст каждого блока (число + метка)
        # Метод textContent() возвращает весь текст внутри элемента
        resume_full_text = home_page.resume_stats_block.text_content()
        vacancies_full_text = home_page.vacancies_stats_block.text_content()
        companies_full_text = home_page.companies_stats_block.text_content()
        print(f"Полный текст статистики резюме: {resume_full_text}")
        print(f"Полный текст статистики вакансий: {vacancies_full_text}")
        print(f"Полный текст статистики компаний: {companies_full_text}")
        # 3. Извлекаем только число из каждого блока
        resume_number_text = home_page.resume_stats_block.locator(".supernova-dashboard-stats__value").text_content()
        vacancies_number_text = home_page.vacancies_stats_block.locator(".supernova-dashboard-stats__value").text_content()
        companies_number_text = home_page.companies_stats_block.locator(".supernova-dashboard-stats__value").text_content()
        print(f"Извлеченное число резюме: {resume_number_text}")
        print(f"Извлеченное число вакансий: {vacancies_number_text}")
        print(f"Извлеченное число компаний: {companies_number_text}")
        expect(home_page.resume_stats_block).to_contain_text("резюме")
        expect(home_page.vacancies_stats_block).to_contain_text("вакансий")
        expect(home_page.companies_stats_block).to_contain_text("компаний")
        assert re.search(r'\d', resume_number_text), "Число резюме не содержит цифр"
        assert re.search(r'\d', vacancies_number_text), "Число вакансий не содержит цифр"
        assert re.search(r'\d', companies_number_text), "Число компаний не содержит цифр"
        # Важно: Не проверяйте точные значения чисел, они меняются!
        print("Тест: Блоки статистических данных видны и их значения извлечены.")

    @pytest.mark.skip
    def test_app_store_link_redirect(self, page: Page):
        """
        Проверяет видимость и кликабельность ссылки "Загрузите в App Store"
        и что клик по ней открывает новую вкладку с ожидаемым URL и элементами.
        """
        home_page = HomePage(page)
        home_page.open()
        try:
            home_page.click_region_ok_button()
            print("Модальное окно подтверждения региона закрыто.")
        except Exception:
             print("Предупреждение: Модалка региона не появилась или не удалось закрыть.")
             pass
        try:
            expect(home_page.registration_modal_title).not_to_be_visible(timeout=10000)
            print("Модальное окно регистрации подтверждено как закрытое.")
        except Exception:
             print("Предупреждение: Модальное окно регистрации все еще видимо или снова появилось после ожидания.")
             pass
        print("Кликаем по ссылке 'Загрузите в App Store' и ожидаем открытия новой страницы...")
        new_page = home_page.click_app_store_link_and_wait_for_page()
        # --- Проверка результата: Верификация новой страницы ---
        print(f"Новая страница открыта. URL: {new_page.url}")
        # 1. Проверяем URL новой страницы
        expected_new_page_url = "https://kaliningrad.hh.ru/mobile?from=main_head&hhtmFromLabel=main_head&hhtmFrom=main"
        # Проверяем URL именно объекта *new_page*
        expect(new_page).to_have_url(expected_new_page_url)
        print(f"Проверка URL новой страницы ({expected_new_page_url}) успешна.")
        # 2. Проверяем видимость ключевых элементов на *новой странице*
        print("Проверка элементов на новой странице...")
        mobile_app_heading = new_page.locator("h1") 
        expect(mobile_app_heading).to_be_visible()
        expect(mobile_app_heading).to_have_text("Мобильное приложение hh.ru") 
        print("Заголовок мобильного приложения виден и корректен.")
        mobile_app_description = new_page.get_by_text("Тысячи вакансий в твоем смартфоне") 
        expect(mobile_app_description).to_be_visible()
        print("Описание 'Тысячи вакансий...' виден.")
        mobile_app_sms_text = new_page.get_by_text("Получите в SMS").first 
        expect(mobile_app_sms_text).to_be_visible()
        print("Текст 'Получите в SMS...' виден.")
        phone_input = new_page.get_by_role("textbox", name="Телефонный номер").first 
        expect(phone_input).to_be_visible()
        expect(phone_input).to_be_enabled() 
        print("Поле ввода номера телефона видно и доступно.")
        get_button = new_page.get_by_role("button", name="Получить").first 
        expect(get_button).to_be_visible()
        expect(get_button).to_be_enabled() 
        print("Кнопка 'Получить' видна и доступна.")
        qrcode_image = new_page.locator(".mob__hh__qrcode").first 
        expect(qrcode_image).to_be_visible()
        print("Изображение QR-кода видно.")
        print("Тест: Ссылка 'Загрузите в App Store' кликнута. Новая вкладка открыта, URL и ключевые элементы проверены успешно.")
        new_page.close()

    @pytest.mark.skip
    def test_google_play_link_redirect(self, page: Page):
        """
        Проверяет видимость и кликабельность ссылки "Доступно в Google Play"
        и что клик по ней открывает новую вкладку с ожидаемым URL и элементами.
        """
        home_page = HomePage(page)
        home_page.open()
        try:
            home_page.click_region_ok_button()
            print("Модальное окно подтверждения региона закрыто.")
        except Exception:
             print("Предупреждение: Модалка региона не появилась или не удалось закрыть.")
             pass
        try:
            expect(home_page.registration_modal_title).not_to_be_visible(timeout=10000)
            print("Модальное окно регистрации подтверждено как закрытое.")
        except Exception:
             print("Предупреждение: Модальное окно регистрации все еще видимо или снова появилось после ожидания.")
             pass
        # >>> Кликаем по ссылке Google Play и получаем объект новой страницы <<<
        print("Кликаем по ссылке 'Доступно в Google Play' и ожидаем открытия новой страницы...")
        new_page = home_page.click_google_play_link_and_wait_for_page()
        # --- Проверка результата: Верификация новой страницы ---
        # Playwright автоматически ожидает загрузки новой страницы
        print(f"Новая страница открыта. URL: {new_page.url}")
        # 1. Проверяем URL новой страницы
        # Используется тот же url, что и для app store. Это может быть неожиданно, что обе ссылки ведут на одну и ту же посадочную страницу,
        # но мы тестируем фактическое поведение сайта.
        expected_new_page_url = "https://kaliningrad.hh.ru/mobile?from=main_head&hhtmFromLabel=main_head&hhtmFrom=main"
        # Проверяем URL именно объекта *new_page*
        expect(new_page).to_have_url(expected_new_page_url)
        print(f"Проверка URL новой страницы ({expected_new_page_url}) успешна.")
        # 2. Проверяем видимость ключевых элементов на *новой странице*
        print("Проверка элементов на новой странице...")
        mobile_app_heading = new_page.locator("h1") 
        expect(mobile_app_heading).to_be_visible()
        expect(mobile_app_heading).to_have_text("Мобильное приложение hh.ru") 
        print("Заголовок мобильного приложения виден и корректен.")
        mobile_app_description = new_page.get_by_text("Тысячи вакансий в твоем смартфоне") 
        expect(mobile_app_description).to_be_visible()
        print("Описание 'Тысячи вакансий...' виден.")
        mobile_app_sms_text = new_page.get_by_text("Получите в SMS").first 
        expect(mobile_app_sms_text).to_be_visible()
        print("Текст 'Получите в SMS...' виден.")
        phone_input = new_page.get_by_role("textbox", name="Телефонный номер").first 
        expect(phone_input).to_be_visible()
        expect(phone_input).to_be_enabled() 
        print("Поле ввода номера телефона видно и доступно.")
        get_button = new_page.get_by_role("button", name="Получить").first 
        expect(get_button).to_be_visible()
        expect(get_button).to_be_enabled() 
        print("Кнопка 'Получить' видна и доступна.")
        qrcode_image = new_page.locator(".mob__hh__qrcode").first 
        expect(qrcode_image).to_be_visible()
        print("Изображение QR-кода видно.")
        print("Тест: Ссылка 'Доступно в Google Play' кликнута. Новая вкладка открыта, URL и ключевые элементы проверены успешно.")
        # >>> Важно: Закрыть новую страницу <<<
        new_page.close()

    @pytest.mark.skip
    def test_app_gallery_link_redirect(self, page: Page):
        """
        Проверяет видимость и кликабельность ссылки "Скачайте в AppGallery"
        и что клик по ней открывает новую вкладку с ожидаемым URL и элементами.
        """
        home_page = HomePage(page)
        home_page.open()
        try:
            home_page.click_region_ok_button()
            print("Модальное окно подтверждения региона закрыто.")
        except Exception:
             print("Предупреждение: Модалка региона не появилась или не удалось закрыть.")
             pass
        try:
            expect(home_page.registration_modal_title).not_to_be_visible(timeout=10000)
            print("Модальное окно регистрации подтверждено как закрытое.")
        except Exception:
             print("Предупреждение: Модальное окно регистрации все еще видимо или снова появилось после ожидания.")
             pass
        # >>> Кликаем по ссылке App Gallery и получаем объект новой страницы <<<
        print("Кликаем по ссылке 'Скачайте в AppGallery' и ожидаем открытия новой страницы...")
        new_page = home_page.click_app_gallery_link_and_wait_for_page()
        # --- Проверка результата: Верификация новой страницы ---
        print(f"Новая страница открыта. URL: {new_page.url}")
        # 1. Проверяем URL новой страницы
        expected_new_page_url = "https://kaliningrad.hh.ru/mobile?from=main_head&hhtmFromLabel=main_head&hhtmFrom=main"
        expect(new_page).to_have_url(expected_new_page_url)
        print(f"Проверка URL новой страницы ({expected_new_page_url}) успешна.")
        # 2. Проверяем видимость ключевых элементов на *новой странице*
        print("Проверка элементов на новой странице...")
        mobile_app_heading = new_page.locator("h1") 
        expect(mobile_app_heading).to_be_visible()
        expect(mobile_app_heading).to_have_text("Мобильное приложение hh.ru") 
        print("Заголовок мобильного приложения виден и корректен.")
        mobile_app_description = new_page.get_by_text("Тысячи вакансий в твоем смартфоне") 
        expect(mobile_app_description).to_be_visible()
        print("Описание 'Тысячи вакансий...' виден.")
        mobile_app_sms_text = new_page.get_by_text("Получите в SMS").first 
        expect(mobile_app_sms_text).to_be_visible()
        print("Текст 'Получите в SMS...' виден.")
        phone_input = new_page.get_by_role("textbox", name="Телефонный номер").first 
        expect(phone_input).to_be_visible()
        expect(phone_input).to_be_enabled() 
        print("Поле ввода номера телефона видно и доступно.")
        get_button = new_page.get_by_role("button", name="Получить").first 
        expect(get_button).to_be_visible()
        expect(get_button).to_be_enabled() 
        print("Кнопка 'Получить' видна и доступна.")
        qrcode_image = new_page.locator(".mob__hh__qrcode").first 
        expect(qrcode_image).to_be_visible()
        print("Изображение QR-кода видно.")
        print("Тест: Ссылка 'Скачайте в AppGallery' кликнута. Новая вкладка открыта, URL и ключевые элементы проверены успешно.")
        new_page.close()

class TestHomePageBlockTwo:
    """Группа тестов для проверки блока ввода номера телефона на главной странице."""

    # @pytest.mark.skip 
    def test_phone_number_block_presence(self, page: Page):
        """
        Проверяет видимость ключевых элементов блока ввода номера телефона:
        заголовка, поля ввода, кнопки "Продолжить", текста соглашения.
        """
        home_page = HomePage(page)
        home_page.open()
        try:
            home_page.click_region_ok_button()
            print("Модальное окно подтверждения региона закрыто.")
        except Exception:
             print("Предупреждение: Модалка региона не появилась или не удалось закрыть.")
             pass
        try:
            expect(home_page.registration_modal_title).not_to_be_visible(timeout=10000)
            print("Модальное окно регистрации подтверждено как закрытое.")
        except Exception:
             print("Предупреждение: Модальное окно регистрации все еще видимо или снова появилось после ожидания.")
             pass
        print("Проверка видимости элементов блока ввода номера телефона...")
        # 1. Проверяем видимость заголовка
        expect(home_page.phone_block_title).to_be_visible()
        expect(home_page.phone_block_title).to_have_text("Напишите телефон, чтобы работодатели могли предложить вам работу")
        print("Заголовок блока виден и корректен.")
        # 2. Проверяем видимость и состояние поля ввода номера телефона
        expect(home_page.phone_number_input).to_be_visible()
        expect(home_page.phone_number_input).to_be_enabled()
        expect(home_page.phone_number_input).to_have_placeholder("Номер телефона")
        print("Поле ввода номера телефона видно, доступно и с корректным плейсхолдером.")
        # 3. Проверяем видимость и состояние кнопки "Продолжить"
        expect(home_page.phone_continue_button).to_be_visible()
        expect(home_page.phone_continue_button).to_be_enabled()
        expect(home_page.phone_continue_button).to_have_text("Продолжить")
        print("Кнопка 'Продолжить' видна, доступна и с корректным текстом.")
        # 4. Проверяем видимость всего блока текста соглашения/политики
        expect(home_page.phone_agreement_policy_text).to_be_visible()
        # Дополнительно можно проверить наличие ключевых фраз в тексте
        expect(home_page.phone_agreement_policy_text).to_contain_text("Нажимая «Продолжить»")
        expect(home_page.phone_agreement_policy_text).to_contain_text("Соглашения об оказании услуг")
        expect(home_page.phone_agreement_policy_text).to_contain_text("политикой конфиденциальности")
        print("Текст соглашения/политики виден и содержит ключевые фразы.")
        print("Тест test_phone_number_block_presence завершен успешно.")
 
    # @pytest.mark.skip
    def test_phone_agreement_link_redirect(self, page: Page):
        """
        Проверяет кликабельность ссылки "Соглашения об оказании услуг..."
        и что клик открывает новую вкладку с ожидаемым URL и элементами на странице соглашения.
        """
        home_page = HomePage(page)
        home_page.open()
        # Обрабатываем начальные модальные окна
        try: home_page.click_region_ok_button(); print("Модалка региона закрыта.")
        except Exception: pass
        try: expect(home_page.registration_modal_title).not_to_be_visible(timeout=10000); print("Модалка регистрации закрыта.")
        except Exception: pass
        # Кликаем по ссылке и получаем объект новой страницы
        print("Кликаем по ссылке 'Соглашения об оказании услуг...' и ожидаем новой страницы...")
        home_page.click_phone_agreement_link_and_wait_for_page()
        expected_agreement_url = "https://hh.ru/account/agreement?backurl=%2Faccount%2Fsignup%3Fbackurl%3D%252F&hhtmFrom=main"
        # 1. Проверяем URL новой страницы
        expect(page).to_have_url(expected_agreement_url)
        print(f"Проверка URL страницы соглашения ({expected_agreement_url}) успешна.")
        # 2. Проверка наличия ключевых элементов на странице соглашения (локаторы от пользователя)
        agreement_heading = page.get_by_role("heading", name="Соглашение по содействию в трудоустройстве и иных видах занятости")
        # Используем частичный текст, так как дата может меняться
        agreement_revision_text = page.get_by_text("(Редакция, действующая с 16.", exact=False) 
        agreement_prev_version_link = page.get_by_role("link", name="ранее действующая редакция")
        expect(agreement_heading).to_be_visible()
        expect(agreement_revision_text).to_be_visible()
        expect(agreement_prev_version_link).to_be_visible()
        print("Ключевые элементы страницы соглашения видны.")

    # @pytest.mark.skip
    def test_phone_policy_link_redirect(self, page: Page):
        """
        Проверяет кликабельность ссылки "политикой конфиденциальности"
        и что клик открывает новую вкладку с ожидаемым URL и элементами на странице политики.
        """
        home_page = HomePage(page)
        home_page.open()
        try: home_page.click_region_ok_button(); print("Модалка региона закрыта.")
        except Exception: pass
        try: expect(home_page.registration_modal_title).not_to_be_visible(timeout=10000); print("Модалка регистрации закрыта.")
        except Exception: pass
        print("Кликаем по ссылке 'политикой конфиденциальности' и ожидаем новой страницы...")
        home_page.click_phone_policy_link_and_wait_for_page()
        expected_policy_url = "https://hh.ru/article/personal_data?backurl=%2F&hhtmFrom=main"
        # 1. Проверяем URL новой страницы
        expect(page).to_have_url(expected_policy_url)
        print(f"Проверка URL страницы политики конфиденциальности ({expected_policy_url}) успешна.")
        # 2. Проверка наличия ключевых элементов на странице политики
        policy_heading = page.get_by_role("heading", name="Политика в области обработки и обеспечения безопасности персональных данных")
        policy_revision_text = page.get_by_text("Редакция от 01 декабря 2024", exact=False) # Используем exact=False для гибкости
        policy_hh_link = page.get_by_role("link", name="Политики в области обработки и обеспечения безопасности персональных данных (hh", exact=False) 
        expect(policy_heading).to_be_visible()
        expect(policy_revision_text).to_be_visible()
        expect(policy_hh_link).to_be_visible()
        print("Ключевые элементы страницы политики конфиденциальности видны.")

    # @pytest.mark.skip
    def test_vacancies_of_the_day_toggle(self, page: Page):
        """
        Проверяет видимость элемента "Вакансии дня" и что клик по нему
        показывает/скрывает соответствующий блок контента.
        """
        home_page = HomePage(page)
        home_page.open()
        try: home_page.click_region_ok_button(); print("Модалка региона закрыта.")
        except Exception: pass
        try: expect(home_page.registration_modal_title).not_to_be_visible(timeout=10000); print("Модалка регистрации закрыта.")
        except Exception: pass
        # 1. Проверяем начальное состояние - контент НЕ должен быть видим
        expect(home_page.vacancies_of_the_day_revealed_content).not_to_be_visible()
        print("'Вакансии дня' контент изначально скрыт.")
        # 2. Проверяем видимость и кликабельность самого элемента-тоггла
        expect(home_page.vacancies_of_the_day_item).to_be_visible()
        expect(home_page.vacancies_of_the_day_item).to_be_enabled()
        print("Элемент 'Вакансии дня' виден и доступен.")
        # 3. Кликаем по элементу, чтобы показать контент
        print("Кликаем по элементу 'Вакансии дня'...")
        home_page.click_vacancies_of_the_day_item()
        # 4. Проверяем, что соответствующий блок контента ПОЯВИЛСЯ
        expect(home_page.vacancies_of_the_day_revealed_content).to_be_visible()
        print("После клика блок контента 'Вакансии дня' появился.")
        # 5. Опционально: Кликнуть еще раз, чтобы скрыть, и проверить, что скрылся
        print("Кликаем по элементу 'Вакансии дня' еще раз, чтобы скрыть контент...")
        home_page.click_vacancies_of_the_day_item()
        expect(home_page.vacancies_of_the_day_revealed_content).not_to_be_visible()
        print("Блок контента скрылся.")

    # @pytest.mark.skip
    def test_companies_of_the_day_toggle(self, page: Page):
        """
        Проверяет видимость элемента "Компании дня" и что клик по нему
        показывает/скрывает соответствующий блок контента.
        """
        home_page = HomePage(page)
        home_page.open()
        try: home_page.click_region_ok_button(); print("Модалка региона закрыта.")
        except Exception: pass
        try: expect(home_page.registration_modal_title).not_to_be_visible(timeout=10000); print("Модалка регистрации закрыта.")
        except Exception: pass
        # 1. Проверяем начальное состояние - контент НЕ должен быть видим
        expect(home_page.companies_of_the_day_revealed_content).not_to_be_visible()
        print("'Компании дня' контент изначально скрыт.")
        # 2. Проверяем видимость и кликабельность самого элемента-тоггла
        expect(home_page.companies_of_the_day_item).to_be_visible()
        expect(home_page.companies_of_the_day_item).to_be_enabled()
        print("Элемент 'Компании дня' виден и доступен.")
        # 3. Кликаем по элементу, чтобы показать контент
        print("Кликаем по элементу 'Компании дня'...")
        home_page.click_companies_of_the_day_item()
        # 4. Проверяем, что соответствующий блок контента ПОЯВИЛСЯ (стал видим)
        expect(home_page.companies_of_the_day_revealed_content).to_be_visible()
        print("После клика блок контента 'Компании дня' появился.")
        # 5. Опционально: Кликнуть еще раз, чтобы скрыть, и проверить, что скрылся
        print("Кликаем по элементу 'Компании дня' еще раз, чтобы скрыть контент...")
        home_page.click_companies_of_the_day_item()
        expect(home_page.companies_of_the_day_revealed_content).not_to_be_visible()
        print("Блок контента скрылся.")

    # @pytest.mark.skip
    def test_work_from_home_link_redirect(self, page: Page):
        """
        Проверяет видимость ссылки "Работа из дома", что клик по ней
        показывает модальное окно регистрации, а затем перенаправляет
        на страницу поиска удаленной работы в том же окне с ожидаемым URL.
        """
        home_page = HomePage(page)
        home_page.open()
        # Обрабатываем начальные модальные окна (регион и регистрация, если появляется сразу)
        try: home_page.click_region_ok_button(); print("Модалка региона закрыта.")
        except Exception: pass
        # Проверяем, что модалка регистрации НЕ видна сразу, если только она не настроена так появляться
        try: expect(home_page.registration_modal_title).not_to_be_visible(timeout=5000); print("Модалка регистрации изначально не видна.")
        except Exception: print("Предупреждение: Модалка регистрации видна сразу после открытия.") 
        # 1. Проверяем видимость и кликабельность ссылки "Работа из дома"
        expect(home_page.work_from_home_link).to_be_visible()
        expect(home_page.work_from_home_link).to_be_enabled()
        print("Ссылка 'Работа из дома' видна и доступна.")
        # 2. Кликаем по ссылке
        print("Кликаем по ссылке 'Работа из дома'...")
        home_page.click_work_from_home_link()
        # --- Ассерт/Обработка: Ожидаем появления модального окна регистрации ПОСЛЕ клика ---
        # Ждем появления заголовка модалки регистрации
        try:
            expect(home_page.registration_modal_title).to_be_visible(timeout=10000) 
            print("Модальное окно регистрации появилось после клика по ссылке 'Работа из дома'.")
            # Кликаем по кнопке закрытия модалки
            print("Закрываем модальное окно регистрации...")
            expect(home_page.registration_modal_close_button).to_be_visible()
            home_page.registration_modal_close_button.click()
            # Ждем, пока модалка исчезнет
            expect(home_page.registration_modal_title).not_to_be_visible(timeout=10000)
            print("Модальное окно регистрации закрыто.")
        except Exception: 
             print("Предупреждение: Модальное окно регистрации не появилось или не удалось закрыть после клика. Продолжаем ожидание навигации.")
        # --- Ассерт: Ожидаем и проверяем Навигацию в ТЕКУЩЕМ окне ---
        # Ждем, пока страница перейдет на ожидаемый URL с путем "/search/vacancy"
        # Playwright's wait_for_url ждет навигации в текущем окне.
        expected_url_path = "/search/vacancy"
        expected_query_params = {'schedule': ['remote'], 'L_profession_id': ['0'], 'area': ['113'], 'hhtmFrom': ['main']}
        print(f"Ожидаем навигацию на путь URL '{expected_url_path}'...")
        # Ждем навигации на URL, который содержит ожидаемый путь, в пределах таймаута
        # "**" в начале позволяет любому домену/субдомену.
        try:
            page.wait_for_url(f"**{expected_url_path}**", timeout=settings.NAVIGATION_TIMEOUT) 
            print(f"Страница навигации ({expected_url_path}) достигнута.")
        except Exception as e:
             print(f"Ошибка ожидания навигации на '{expected_url_path}': {e}")
             # Добавьте ассерт False, чтобы тест упал явно, если навигация не произошла
             assert False, f"Не удалось перейти на ожидаемую страницу после клика по ссылке 'Работа из дома'. Текущий URL: {page.url}"
        # Теперь, когда навигация завершена, проверяем полный URL (путь и параметры запроса)
        current_url = page.url # Проверяем URL текущего объекта page (того же окна)
        parsed_url = urlparse(current_url)
        # Проверяем путь URL
        assert parsed_url.path == expected_url_path, f"Ожидаемый путь URL: {expected_url_path}, Фактический путь URL: {parsed_url.path}"
        print(f"Путь URL '{expected_url_path}' корректен.")
        # Проверяем параметры запроса
        current_query_params = parse_qs(parsed_url.query)
        # Сравниваем словари параметров. Используем sorted(items()) для устойчивости к порядку параметров.
        assert sorted(current_query_params.items()) == sorted(expected_query_params.items()), f"Ожидаемые параметры запроса: {expected_query_params}, Фактические параметры запроса: {current_query_params}"
        print(f"Параметры запроса {expected_query_params} корректны.")

    # @pytest.mark.skip
    def test_part_time_toggle(self, page: Page):
        """
        Проверяет видимость элемента "Подработка" и что клик по нему
        показывает/скрывает соответствующий блок контента.
        """
        home_page = HomePage(page)
        home_page.open()
        try: home_page.click_region_ok_button(); print("Модалка региона закрыта.")
        except Exception: pass
        try: expect(home_page.registration_modal_title).not_to_be_visible(timeout=10000); print("Модалка регистрации закрыта.")
        except Exception: pass
        # 1. Проверяем начальное состояние - контент НЕ должен быть видим
        expect(home_page.part_time_revealed_content).not_to_be_visible()
        print("'Подработка' контент изначально скрыт.")
        # 2. Проверяем видимость и кликабельность самого элемента-тоггла
        expect(home_page.part_time_item).to_be_visible()
        expect(home_page.part_time_item).to_be_enabled()
        print("Элемент 'Подработка' виден и доступен.")
        # 3. Кликаем по элементу, чтобы показать контент
        print("Кликаем по элементу 'Подработка'...")
        home_page.click_part_time_item()
        # 4. Проверяем, что соответствующий блок контента ПОЯВИЛСЯ (стал видим)
        expect(home_page.part_time_revealed_content).to_be_visible()
        print("После клика блок контента 'Подработка' появился.")
        # 5. Опционально: Кликнуть еще раз, чтобы скрыть, и проверить, что скрылся
        print("Кликаем по элементу 'Подработка' еще раз, чтобы скрыть контент...")
        home_page.click_part_time_item()
        expect(home_page.part_time_revealed_content).not_to_be_visible()
        print("Блок контента скрылся.")

    # @pytest.mark.skip
    def test_courier_item_toggle(self, page: Page):
        """
        Проверяет видимость карточки "Курьер" и что клик по ней
        показывает/скрывает соответствующий блок контента.
        """
        home_page = HomePage(page)
        home_page.open()
        try: home_page.click_region_ok_button(); print("Модалка региона закрыта.")
        except Exception: pass
        try: expect(home_page.registration_modal_title).not_to_be_visible(timeout=10000); print("Модалка регистрации закрыта.")
        except Exception: pass
        # 1. Проверяем начальное состояние - контент НЕ должен быть видим
        expect(home_page.courier_revealed_content).not_to_be_visible()
        print("'Курьер' контент изначально скрыт.")
        # 2. Проверяем видимость и кликабельность самой карточки
        expect(home_page.courier_item).to_be_visible()
        expect(home_page.courier_item).to_be_enabled()
        print("Карточка 'Курьер' видна и доступна.")
        # 3. Кликаем по карточке, чтобы показать контент
        print("Кликаем по карточке 'Курьер'...")
        home_page.click_courier_item()
        # 4. Проверяем, что соответствующий блок контента ПОЯВИЛСЯ (стал видим)
        expect(home_page.courier_revealed_content).to_be_visible()
        print("После клика блок контента 'Курьер' появился.")
        # 5. Опционально: Кликнуть еще раз, чтобы скрыть, и проверить, что скрылся
        print("Кликаем по карточке 'Курьер' еще раз, чтобы скрыть контент...")
        home_page.click_courier_item()
        expect(home_page.courier_revealed_content).not_to_be_visible()
        print("Блок контента скрылся.")

    # @pytest.mark.skip
    def test_programmer_item_toggle(self, page: Page):
        """
        Проверяет видимость карточки "Программист" и что клик по ней
        показывает/скрывает соответствующий блок контента.
        """
        home_page = HomePage(page)
        home_page.open()
        try: home_page.click_region_ok_button(); print("Модалка региона закрыта.")
        except Exception: pass
        try: expect(home_page.registration_modal_title).not_to_be_visible(timeout=10000); print("Модалка регистрации закрыта.")
        except Exception: pass
        # 1. Check initial state - content should NOT be visible
        expect(home_page.programmer_revealed_content).not_to_be_visible()
        print("'Программист' контент изначально скрыт.")
        # 2. Check visibility and clickability of the item
        expect(home_page.programmer_item).to_be_visible()
        expect(home_page.programmer_item).to_be_enabled()
        print("Карточка 'Программист' видна и доступна.")
        # 3. Click the item to reveal content
        print("Кликаем по карточке 'Программист'...")
        home_page.click_programmer_item()
        # 4. Assert that the corresponding content block appears (becomes visible)
        expect(home_page.programmer_revealed_content).to_be_visible()
        print("После клика блок контента 'Программист' появился.")
        # 5. Optional: Click again to hide and assert it's not visible
        print("Кликаем по карточке 'Программист' еще раз, чтобы скрыть контент...")
        home_page.click_programmer_item()
        expect(home_page.programmer_revealed_content).not_to_be_visible()
        print("Блок контента скрылся.")

    # @pytest.mark.skip
    def test_manager_item_toggle(self, page: Page):
        """
        Проверяет видимость карточки "Менеджер" и что клик по ней
        показывает/скрывает соответствующий блок контента.
        """
        home_page = HomePage(page)
        home_page.open()
        try: home_page.click_region_ok_button(); print("Модалка региона закрыта.")
        except Exception: pass
        try: expect(home_page.registration_modal_title).not_to_be_visible(timeout=10000); print("Модалка регистрации закрыта.")
        except Exception: pass
        # 1. Check initial state - content should NOT be visible
        expect(home_page.manager_revealed_content).not_to_be_visible()
        print("'Менеджер' контент изначально скрыт.")
        # 2. Проверяем видимость и кликабельность самой карточки
        expect(home_page.manager_item).to_be_visible()
        expect(home_page.manager_item).to_be_enabled()
        print("Карточка 'Менеджер' видна и доступна.")
        # 3. Кликаем по карточке, чтобы показать контент
        print("Кликаем по карточке 'Менеджер'...")
        home_page.click_manager_item()
        # 4. Assert that the corresponding content block appears (becomes visible)
        expect(home_page.manager_revealed_content).to_be_visible()
        print("После клика блок контента 'Менеджер' появился.")
        # 5. Optional: Кликнуть еще раз, чтобы скрыть, и проверить, что скрылся
        print("Кликаем по карточке 'Менеджер' еще раз, чтобы скрыть контент...")
        home_page.click_manager_item()
        expect(home_page.manager_revealed_content).not_to_be_visible()
        print("Блок контента скрылся.")    

    # @pytest.mark.skip
    def test_show_more_professions_toggle(self, page: Page):
        """
        Проверяет видимость кнопки "Ещё 23 профессии" и что клик по ней
        показывает дополнительные карточки профессий.
        """
        home_page = HomePage(page)
        home_page.open()
        try: home_page.click_region_ok_button(); print("Модалка региона закрыта.")
        except Exception: pass
        try: expect(home_page.registration_modal_title).not_to_be_visible(timeout=10000); print("Модалка регистрации закрыта.")
        except Exception: pass
        # 1. Проверяем начальное состояние - контейнер с дополнительными карточками НЕ должен быть видим
        expect(home_page.additional_professions_container).not_to_be_visible()
        print("'Ещё профессии' дополнительный контент изначально скрыт.")
        # 2. Проверяем видимость и кликабельность самой кнопки
        expect(home_page.show_more_professions_button).to_be_visible()
        expect(home_page.show_more_professions_button).to_be_enabled()
        print("Кнопка 'Ещё 23 профессии' видна и доступна.")
        # 3. Кликаем по кнопке, чтобы показать контент
        print("Кликаем по кнопке 'Ещё 23 профессии'...")
        home_page.click_show_more_professions_button()
        home_page.additional_professions_container_click.click()
        expect(home_page.additional_professions_container).to_be_visible()
        print("После клика блок контента 'Ещё 23 профессии' появился.")

class TestHomePageBlockThree:

    # @pytest.mark.skip
    def test_hh_pro_banner_redirect(self, page: Page):
        """
        Проверяет видимость баннерной ссылки "Ищите работу эффективнее"
        и что клик по ней открывает новую вкладку с ожидаемым URL.
        """
        home_page = HomePage(page)
        home_page.open()
        try: home_page.click_region_ok_button(); print("Модалка региона закрыта.")
        except Exception: pass
        try: expect(home_page.registration_modal_title).not_to_be_visible(timeout=10000); print("Модалка регистрации закрыта.")
        except Exception: pass
        # 1. Проверяем видимость и кликабельность баннерной ссылки
        print("Ожидаем видимость и доступность баннерной ссылки 'Ищите работу эффективнее'...")
        # 2. Кликаем по ссылке и получаем объект новой страницы (ждем открытия новой вкладки)
        print("Кликаем по баннерной ссылке 'Ищите работу эффективнее' и ожидаем новой вкладки...")
        new_page = home_page.click_hh_pro_banner_link_and_wait_for_page()
        expected_hh_pro_url = "https://kaliningrad.hh.ru/applicant-services/hhpro"
        # 1. Проверяем URL новой страницы
        expect(new_page).to_have_url(expected_hh_pro_url)
        print(f"Проверка URL новой страницы HH Pro ({expected_hh_pro_url}) успешна.")
        # 2. Опционально: Проверить наличие ключевых элементов на странице HH Pro для уверенности
        expect(new_page.get_by_role("heading", name="Работа найдётся скорее с hh")).to_be_visible()
        expect(new_page.get_by_role("button", name="Подключить 199 ₽ в неделю").first).to_be_visible()
        # 3. Закрываем новую страницу
        new_page.close()
        print("Тест test_hh_pro_banner_redirect завершен успешно.")

    # @pytest.mark.skip
    def test_work_in_kaliningrad_title_presence(self, page: Page):
        """
        Проверяет видимость и текст статического заголовка "Работа в Калининграде".
        """
        home_page = HomePage(page)
        home_page.open()
        try: home_page.click_region_ok_button(); print("Модалка региона закрыта.")
        except Exception: pass
        try: expect(home_page.registration_modal_title).not_to_be_visible(timeout=10000); print("Модалка регистрации закрыта.")
        except Exception: pass
        # 1. Проверяем видимость заголовка
        expect(home_page.work_in_kaliningrad_title).to_be_visible()
        print("Заголовок 'Работа в Калининграде' виден.")
        # 2. Проверяем текст заголовка
        # Используем regex для проверки текста, как в локаторе
        expect(home_page.work_in_kaliningrad_title).to_have_text(re.compile(r"^Работа в Калининграде$"))
        print("Текст заголовка 'Работа в Калининграде' корректен.")

    # @pytest.mark.skip
    def test_work_in_kaliningrad_list_presence_and_count(self, page: Page):
        """
        Проверяет видимость (части) списка "Работа в Калининграде"
        и наличие в нем элементов (ссылок).
        """
        home_page = HomePage(page)
        home_page.open()
        try: home_page.click_region_ok_button(); print("Модалка региона закрыта.")
        except Exception: pass
        try: expect(home_page.registration_modal_title).not_to_be_visible(timeout=10000); print("Модалка регистрации закрыта.")
        except Exception: pass
        # 1. Проверяем видимость (части) контейнера списка
        expect(home_page.work_in_kaliningrad_partial_list_container).to_be_visible(timeout=10000) # Увеличим таймаут на всякий случай
        print("(Часть) списка 'Работа в Калининграде' видна.")
        # 2. Проверяем наличие элементов (ссылок) в этой части списка
        list_items_locator = home_page.work_in_kaliningrad_partial_list_container.locator("a") 
        expect(list_items_locator).to_have_count(lambda count: count > 0, timeout=10000) 
        print(f"В (части) списка 'Работа в Калининграде' найдено {list_items_locator.count()} элементов.")

    # @pytest.mark.skip
    def test_vacancies_of_the_day_kaliningrad_title_presence(self, page: Page):
        """
        Проверяет видимость и текст статического заголовка "Вакансии дня в Калининграде".
        """
        home_page = HomePage(page)
        home_page.open()
        try: home_page.click_region_ok_button(); print("Модалка региона закрыта.")
        except Exception: pass
        try: expect(home_page.registration_modal_title).not_to_be_visible(timeout=10000); print("Модалка регистрации закрыта.")
        except Exception: pass
        # 1. Проверяем видимость заголовка
        expect(home_page.vacancies_of_the_day_kaliningrad_title).to_be_visible()
        print("Заголовок 'Вакансии дня в Калининграде' виден.")
        # 2. Проверяем текст заголовка
        expect(home_page.vacancies_of_the_day_kaliningrad_title).to_have_text("Вакансии дня в Калининграде")
        print("Текст заголовка 'Вакансии дня в Калининграде' корректен.")

    # @pytest.mark.skip
    def test_vacancies_list_presence_and_count(self, page: Page):
        """
        Проверяет видимость контейнера списка вакансий "Вакансии дня в Калининграде"
        и наличие в нем элементов (ссылок).
        """
        home_page = HomePage(page)
        home_page.open()
        try: home_page.click_region_ok_button(); print("Модалка региона закрыта.")
        except Exception: pass
        try: expect(home_page.registration_modal_title).not_to_be_visible(timeout=10000); print("Модалка регистрации закрыта.")
        except Exception: pass
        # 1. Проверяем видимость контейнера списка вакансий
        expect(home_page.vacancies_list_container).to_be_visible(timeout=10000)
        print("Контейнер списка вакансий 'Вакансии дня в Калининграде' виден.")
        # 2. Проверяем наличие элементов (ссылок) в списке
        expect(home_page.vacancies_list_item_links).to_have_count(lambda count: count > 0, timeout=10000) 
        print(f"В списке вакансий найдено {home_page.vacancies_list_item_links.count()} элементов.")

    # @pytest.mark.skip
    def test_first_vacancy_link_redirect(self, page: Page):
        """
        Находит первую ссылку вакансии в списке "Вакансии дня в Калининграде",
        кликает по ней и проверяет, что открывается новая вкладка со страницей вакансии
        с ожидаемым форматом URL (/vacancy/ID) И наличием элемента заголовка вакансии.
        """
        home_page = HomePage(page)
        home_page.open()
        try: home_page.click_region_ok_button(); print("Модалка региона закрыта.")
        except Exception: pass
        try: expect(home_page.registration_modal_title).not_to_be_visible(timeout=10000); print("Модалка регистрации закрыта.")
        except Exception: pass
        # 1. Кликаем по первой ссылке в списке (метод уже ожидает новую вкладку и проверяет наличие элементов)
        # Метод click_first_vacancy_list_item_and_wait_for_page сам проверяет, что в списке есть элементы и кликает первую.
        print("Кликаем по первой ссылке в списке вакансий и ожидаем новой вкладки...")
        new_page = home_page.click_first_vacancy_list_item_and_wait_for_page()
        # --- Ассерт на новой странице (Страница вакансии) ---
        # Ожидаемый формат URL страницы вакансии: https://kaliningrad.hh.ru/vacancy/ID
        # Проверяем путь URL и что он начинается с "/vacancy/" и далее идет числовой ID.
        expected_url_path_prefix = "/vacancy/"
        print(f"Проверяем URL новой страницы. Ожидаемый путь начинается с '{expected_url_path_prefix}'...")
        # Проверяем URL новой страницы (объекта new_page)
        current_url = new_page.url
        parsed_url = urlparse(current_url)
        # Проверяем, что путь URL начинается с /vacancy/
        assert parsed_url.path.startswith(expected_url_path_prefix), f"Ожидаемый путь URL начинается с: {expected_url_path_prefix}, Фактический путь URL: {parsed_url.path}"
        # Опционально, проверяем, что после "/vacancy/" идет числовой ID
        vacancy_id = parsed_url.path.replace(expected_url_path_prefix, "")
        assert vacancy_id.isdigit(), f"ID вакансии в URL '{vacancy_id}' не является числовым."
        print(f"URL страницы вакансии корректен (путь начинается с '{expected_url_path_prefix}' и содержит числовой ID).")
        # 2. НОВАЯ ПРОВЕРКА: Проверяем наличие ключевого элемента на странице вакансии
        # Используем локатор для h1 с атрибутом data-qa="vacancy-title", который вы предоставили.
        # Этот локатор надежен и не зависит от конкретного названия вакансии.
        vacancy_heading_element = new_page.locator('h1[data-qa="vacancy-title"]')
        # Проверяем, что этот элемент виден на новой странице в пределах таймаута.
        expect(vacancy_heading_element).to_be_visible(timeout=10000)
        print("На новой странице вакансии успешно найден элемент заголовка вакансии (h1 с data-qa='vacancy-title').")
        # 3. Закрываем новую страницу
        new_page.close()
        print("Тест test_first_vacancy_link_redirect завершен успешно.")

class TestHomePageBlockFour:

    # @pytest.mark.skip
    def test_work_in_professions_title_link_redirect(self, page: Page):
        """
        Проверяет видимость ссылки заголовка "Работа по профессиям в Калининграде"
        и что клик по ней перенаправляет на общую страницу вакансий в том же окне.
        """
        home_page = HomePage(page)
        home_page.open()
        # Обрабатываем начальные модальные окна
        try: home_page.click_region_ok_button(); print("Модалка региона закрыта.")
        except Exception: pass
        try: expect(home_page.registration_modal_title).not_to_be_visible(timeout=10000); print("Модалка регистрации закрыта.")
        except Exception: pass
        # 1. Проверяем видимость и кликабельность ссылки заголовка
        expect(home_page.work_in_professions_title_link).to_be_visible()
        expect(home_page.work_in_professions_title_link).to_be_enabled()
        print("Ссылка заголовка 'Работа по профессиям в Калининграде' видна и доступна.")
        # 2. Кликаем по ссылке
        print("Кликаем по ссылке заголовка 'Работа по профессиям в Калининграде'...")
        home_page.click_work_in_professions_title_link()
        # --- Ассерт: Ожидаем и проверяем Навигацию в ТЕКУЩЕМ окне ---
        expected_url = "https://kaliningrad.hh.ru/vacancies?hhtmFrom=main"
        print(f"Ожидаем навигацию на URL: {expected_url}")
        try:
            # wait_for_url ждет навигации в текущем окне.
            page.wait_for_url(expected_url, timeout=settings.NAVIGATION_TIMEOUT) 
            print(f"Страница навигации ({expected_url}) достигнута.")
        except Exception as e:
             print(f"Ошибка ожидания навигации: {e}")
             assert False, f"Не удалось перейти на ожидаемую страницу после клика по ссылке заголовка. Текущий URL: {page.url}"
        # 3. Опционально: Проверить наличие элементов на странице назначения
        expected_heading_on_target_page = page.get_by_role("heading", name="Работа и вакансии по профессии в Калининграде")
        expect(expected_heading_on_target_page).to_be_visible(timeout=10000)
        print("На странице назначения найден ожидаемый заголовок 'Работа и вакансии по профессии в Калининграде'.")
        # Можно также проверить наличие заголовка "Специализации"
        specializations_heading = page.get_by_role("heading", name="Специализации")
        expect(specializations_heading).to_be_visible(timeout=10000)
        print("На странице назначения найден заголовок 'Специализации'.")
        print("Тест test_work_in_professions_title_link_redirect завершен успешно.")

    # @pytest.mark.skip
    def test_work_in_professions_list_presence_and_count(self, page: Page):
        """
        Проверяет видимость контейнера списка профессий и наличие в нем элементов (ссылок).
        """
        home_page = HomePage(page)
        home_page.open()
        # Обрабатываем начальные модальные окна
        try: home_page.click_region_ok_button(); print("Модалка региона закрыта.")
        except Exception: pass
        try: expect(home_page.registration_modal_title).not_to_be_visible(timeout=10000); print("Модалка регистрации закрыта.")
        except Exception: pass
        # 1. Проверяем видимость контейнера списка профессий
        expect(home_page.work_in_professions_list_container).to_be_visible(timeout=10000)
        print("Контейнер списка профессий 'Работа по профессиям в Калининграде' виден.")
        # 2. Проверяем наличие элементов (ссылок профессий) в списке
        # Локатор work_in_professions_item_links ищет все ссылки внутри контейнера.
        # Ожидаем, что в списке будет хотя бы 1 элемент (ссылка)
        expect(home_page.work_in_professions_item_links).to_have_count(lambda count: count > 0, timeout=10000) 
        # Можно ожидать конкретное минимальное число, если известно из анализа
        print(f"В списке профессий найдено {home_page.work_in_professions_item_links.count()} элементов.")

    # @pytest.mark.skip
    def test_first_profession_link_redirect(self, page: Page):
        """
        Находит первую ссылку профессии в списке "Работа по профессиям в Калининграде",
        кликает по ней, обрабатывает модальное окно регистрации, и проверяет,
        что происходит перенаправление на страницу поиска вакансий по профессии с ожидаемым форматом URL.
        """
        home_page = HomePage(page)
        home_page.open()
        try: home_page.click_region_ok_button(); print("Модалка региона закрыта.")
        except Exception: pass
        try: expect(home_page.registration_modal_title).not_to_be_visible(timeout=5000); print("Модалка регистрации изначально не видна.")
        except Exception: print("Предупреждение: Модалка регистрации видна сразу после открытия.")
        # 1. Кликаем по первой ссылке в списке профессий и обрабатываем модальное окно
        # Метод click_first_work_in_professions_list_item_and_handle_modal сам обрабатывает модалку и кликает первую ссылку.
        print("Кликаем по первой ссылке профессии в списке...")
        home_page.click_first_work_in_professions_list_item_and_handle_modal(page)
        # --- Ассерт: Ожидаем и проверяем Навигацию в ТЕКУЩЕМ окне ---
        # Проверяем путь URL и что он начинается с "/search/vacancy".
        # Также проверяем наличие ключевых параметров запроса (area и professional_role).
        expected_url_path = "/search/vacancy"
        print(f"Ожидаем навигацию на путь URL '{expected_url_path}' с ключевыми параметрами...")
        try:
            # wait_for_url может использовать регулярные выражения.
            # Проверяем, что URL начинается с пути, содержит параметр 'area=\d+', и содержит параметр 'professional_role='.
            # Порядок параметров может быть разным, поэтому используем .* между ними.
            page.wait_for_url(re.compile(rf"**{expected_url_path}.*area=\d+.*professional_role=.*"), timeout=settings.NAVIGATION_TIMEOUT) 
            print(f"Страница навигации (путь '{expected_url_path}' с параметрами area и professional_role) достигнута.")
        except Exception as e:
             print(f"Ошибка ожидания навигации: {e}")
             assert False, f"Не удалось перейти на ожидаемую страницу поиска по профессии. Текущий URL: {page.url}"
        print("Тест test_first_profession_link_redirect завершен успешно.")

    # @pytest.mark.skip
    def test_messenger_title_presence(self, page: Page):
        """
        Проверяет видимость и текст статического заголовка "Вакансии в мессенджере".
        """
        home_page = HomePage(page)
        home_page.open()
        try: home_page.click_region_ok_button(); print("Модалка региона закрыта.")
        except Exception: pass
        try: expect(home_page.registration_modal_title).not_to_be_visible(timeout=10000); print("Модалка регистрации закрыта.")
        except Exception: pass
        expect(home_page.messenger_title).to_be_visible()
        expect(home_page.messenger_title).to_have_text("Вакансии в мессенджере")
        print("Заголовок 'Вакансии в мессенджере' виден и текст корректен.")

    # @pytest.mark.skip
    def test_messenger_qr_code_presence(self, page: Page):
        """
        Проверяет видимость изображения QR-кода в блоке "Вакансии в мессенджере".
        """
        home_page = HomePage(page)
        home_page.open()
        try: home_page.click_region_ok_button(); print("Модалка региона закрыта.")
        except Exception: pass
        try: expect(home_page.registration_modal_title).not_to_be_visible(timeout=10000); print("Модалка регистрации закрыта.")
        except Exception: pass
        expect(home_page.messenger_qr_code_image).to_be_visible()
        print("Изображение QR-кода в блоке 'Вакансии в мессенджере' видно.")

    # @pytest.mark.skip
    def test_messenger_static_text_presence(self, page: Page):
        """
        Проверяет видимость и текст статического текста под QR-кодом
        в блоке "Вакансии в мессенджере".
        """
        home_page = HomePage(page)
        home_page.open()
        try: home_page.click_region_ok_button(); print("Модалка региона закрыта.")
        except Exception: pass
        try: expect(home_page.registration_modal_title).not_to_be_visible(timeout=10000); print("Модалка регистрации закрыта.")
        except Exception: pass
        expect(home_page.messenger_static_text).to_be_visible()
        expect(home_page.messenger_static_text).to_have_text("Чтобы подключить сервис на телефоне, наведите камеру на QR-код")
        print("Статический текст под QR-кодом виден и текст корректен.")

    # @pytest.mark.skip
    def test_messenger_vk_link_redirect(self, page: Page):
        """
        Проверяет видимость ссылки VK и что клик по ней открывает новую вкладку с ожидаемым URL.
        """
        home_page = HomePage(page)
        home_page.open()
        try: home_page.click_region_ok_button(); print("Модалка региона закрыта.")
        except Exception: pass
        try: expect(home_page.registration_modal_title).not_to_be_visible(timeout=10000); print("Модалка регистрации закрыта.")
        except Exception: pass
        expect(home_page.messenger_vk_link).to_be_visible()
        expect(home_page.messenger_vk_link).to_be_enabled()
        print("Ссылка VK видна и доступна.")
        print("Кликаем по ссылке VK и ожидаем новой вкладки...")
        new_page = home_page.click_messenger_vk_link_and_wait_for_page()
        # --- Ассерт на новой странице (VK) ---
        expected_url_prefix = "https://vk.me/headhunter"
        print(f"Проверяем URL новой страницы VK. Ожидаемый URL начинается с '{expected_url_prefix}'...")
        # Используем expect(new_page).to_have_url с регулярным выражением, чтобы учесть возможные параметры запроса
        expect(new_page).to_have_url(re.compile(rf"^{re.escape(expected_url_prefix)}.*"), timeout=settings.NAVIGATION_TIMEOUT) # re.escape экранирует спецсимволы в URL
        print(f"URL новой страницы VK корректен (начинается с '{expected_url_prefix}').")
        new_page.close()
        print("Тест test_messenger_vk_link_redirect завершен успешно.")

    # @pytest.mark.skip
    def test_messenger_telegram_link_redirect(self, page: Page):
        """
        Проверяет видимость ссылки Telegram, обрабатывает браузерный диалог
        (нажимает "Отмена") и проверяет, что открывается новая вкладка
        с ожидаемым URL и модальным окном "Ничего не происходит?".
        """
        home_page = HomePage(page)
        home_page.open()
        try: home_page.click_region_ok_button(); print("Модалка региона закрыта.")
        except Exception: pass
        try: expect(home_page.registration_modal_title).not_to_be_visible(timeout=10000); print("Модалка регистрации закрыта.")
        except Exception: pass
        expect(home_page.messenger_telegram_link).to_be_visible()
        expect(home_page.messenger_telegram_link).to_be_enabled()
        print("Ссылка Telegram видна и доступна.")
        # Кликаем по ссылке, обрабатываем диалог и получаем объект новой страницы (ждем новой вкладки)
        # Обработка диалога происходит внутри метода click_messenger_telegram_link_and_wait_for_page.
        print("Кликаем по ссылке Telegram, ожидаем браузерный диалог и новую вкладку...")
        new_page = home_page.click_messenger_telegram_link_and_wait_for_page()
        # --- Ассерт на новой странице (Модальное окно предложения Telegram) ---
        expected_url_prefix = "https://chatbot.hh.ru/hh-bot/telegram"
        print(f"Проверяем URL новой страницы Telegram. Ожидаемый URL начинается с '{expected_url_prefix}'...")
        expect(new_page).to_have_url(re.compile(rf"^{re.escape(expected_url_prefix)}.*"), timeout=settings.NAVIGATION_TIMEOUT)
        print(f"URL новой страницы Telegram корректен (начинается с '{expected_url_prefix}').")
        # Проверяем наличие модального окна "Ничего не происходит?" на новой странице
        messenger_modal_heading_on_new_page = new_page.getByRole("heading", name="Ничего не происходит?")
        expect(messenger_modal_heading_on_new_page).to_be_visible(timeout=10000)
        print("На новой странице Telegram найдено модальное окно 'Ничего не происходит?'.")
        # Опционально: Проверить наличие QR кода внутри модального окна на новой странице
        messenger_modal_qr_code_on_new_page = new_page.locator(".suggestion-modal__qr-code")
        expect(messenger_modal_qr_code_on_new_page).to_be_visible(timeout=10000)
        new_page.close()
        print("Тест test_messenger_telegram_link_redirect завершен успешно.")

    # @pytest.mark.skip
    def test_messenger_viber_link_redirect(self, page: Page):
        """
        Проверяет видимость ссылки Viber и что клик по ней открывает новую вкладку
        с ожидаемым URL и модальным окном "Ничего не происходит?".
        Браузерный диалог НЕ ожидается.
        """
        home_page = HomePage(page)
        home_page.open()
        try: home_page.click_region_ok_button(); print("Модалка региона закрыта.")
        except Exception: pass
        try: expect(home_page.registration_modal_title).not_to_be_visible(timeout=10000); print("Модалка регистрации закрыта.")
        except Exception: pass
        expect(home_page.messenger_viber_link).to_be_visible()
        expect(home_page.messenger_viber_link).to_be_enabled()
        print("Ссылка Viber видна и доступна.")
        # Кликаем по ссылке и получаем объект новой страницы (ждем новой вкладки)
        # Браузерный диалог НЕ ожидается для Viber.
        print("Кликаем по ссылке Viber и ожидаем новой вкладки...")
        new_page = home_page.click_messenger_viber_link_and_wait_for_page()
        # --- Ассерт на новой странице (Модальное окно предложения Viber) ---
        expected_url_prefix = "https://chatbot.hh.ru/hh-bot/viber"
        print(f"Проверяем URL новой страницы Viber. Ожидаемый URL начинается с '{expected_url_prefix}'...")
        expect(new_page).to_have_url(re.compile(rf"^{re.escape(expected_url_prefix)}.*"), timeout=settings.NAVIGATION_TIMEOUT)
        print(f"URL новой страницы Viber корректен (начинается с '{expected_url_prefix}').")
        # Проверяем наличие модального окна "Ничего не происходит?" на новой странице
        # Локатор этого заголовка специфичен для этой новой страницы.
        messenger_modal_heading_on_new_page = new_page.getByRole("heading", name="Ничего не происходит?")
        expect(messenger_modal_heading_on_new_page).to_be_visible(timeout=10000)
        print("На новой странице Viber найдено модальное окно 'Ничего не происходит?'.")
        # Опционально: Проверить наличие QR кода внутри модального окна на новой странице
        messenger_modal_qr_code_on_new_page = new_page.locator(".suggestion-modal__qr-code")
        expect(messenger_modal_qr_code_on_new_page).to_be_visible(timeout=10000)
        new_page.close()
        print("Тест test_messenger_viber_link_redirect завершен успешно.")

    # @pytest.mark.skip
    def test_news_title_link_redirect(self, page: Page):
        """
        Проверяет видимость ссылки заголовка "Новости" и что клик по ней
        перенаправляет на страницу новостей сайта в том же окне.
        """
        home_page = HomePage(page)
        home_page.open()
        try: home_page.click_region_ok_button(); print("Модалка региона закрыта.")
        except Exception: pass
        try: expect(home_page.registration_modal_title).not_to_be_visible(timeout=10000); print("Модалка регистрации закрыта.")
        except Exception: pass
        # 1. Проверяем видимость и кликабельность ссылки заголовка
        expect(home_page.news_title_link).to_be_visible()
        expect(home_page.news_title_link).to_be_enabled()
        print("Ссылка заголовка 'Новости' видна и доступна.")
        # 2. Кликаем по ссылке
        print("Кликаем по ссылке заголовка 'Новости'...")
        home_page.click_news_title_link()
        # --- Ассерт: Ожидаем и проверяем Навигацию в ТЕКУЩЕМ окне ---
        expected_url = "https://kaliningrad.hh.ru/articles/site-news?hhtmFrom=main"
        print(f"Ожидаем навигацию на URL: {expected_url}")
        try:
            page.wait_for_url(expected_url, timeout=settings.NAVIGATION_TIMEOUT) 
            print(f"Страница навигации ({expected_url}) достигнута.")
        except Exception as e:
             print(f"Ошибка ожидания навигации: {e}")
             assert False, f"Не удалось перейти на ожидаемую страницу новостей сайта после клика по ссылке заголовка. Текущий URL: {page.url}"
        # 3. Опционально: Проверить наличие элементов на странице назначения (страница новостей сайта)
        expected_heading_on_target_page = page.getByRole("heading", name="Новости сайта")
        expect(expected_heading_on_target_page).to_be_visible(timeout=10000)
        print("На странице назначения найден ожидаемый заголовок 'Новости сайта'.")
        # Можно также проверить наличие элемента списка новостей на странице назначения, используя второй локатор
        news_list_element_on_target_page = page.locator(".bloko-column > div:nth-child(4)")
        expect(news_list_element_on_target_page).to_be_visible(timeout=10000)
        print("Тест test_news_title_link_redirect завершен успешно.")

    # @pytest.mark.skip
    def test_news_list_presence_and_count(self, page: Page):
        """
        Проверяет видимость контейнера списка новостей и наличие в нем элементов (ссылок).
        """
        home_page = HomePage(page)
        home_page.open()
        try: home_page.click_region_ok_button(); print("Модалка региона закрыта.")
        except Exception: pass
        try: expect(home_page.registration_modal_title).not_to_be_visible(timeout=10000); print("Модалка регистрации закрыта.")
        except Exception: pass
        # 1. Проверяем видимость контейнера списка новостей
        expect(home_page.news_block_container).to_be_visible(timeout=10000) # Проверяем видимость всего блока новостей
        expect(home_page.news_list_container).to_be_visible(timeout=10000) # Проверяем видимость самого списка ul
        print("Контейнер списка новостей 'Новости' виден.")
        # 2. Проверяем наличие элементов (ссылок новостей) в списке
        # Ожидаем, что в списке будет хотя бы 1 элемент (ссылка)
        expect(home_page.news_item_links).to_have_count(lambda count: count > 0, timeout=10000) 
        # Oжидаем минимум 3 элемента:
        expect(home_page.news_item_links).to_have_count(lambda count: count >= 3, timeout=10000)
        print(f"В списке новостей найдено {home_page.news_item_links.count()} элементов.")

    # @pytest.mark.skip
    def test_first_news_link_redirect(self, page: Page):
        """
        Находит первую ссылку новости в списке "Новости",
        кликает по ней и проверяет, что происходит перенаправление на страницу новости
        с ожидаемым форматом URL (/article/ID...).
        """
        home_page = HomePage(page)
        home_page.open()
        try: home_page.click_region_ok_button(); print("Модалка региона закрыта.")
        except Exception: pass
        try: expect(home_page.registration_modal_title).not_to_be_visible(timeout=10000); print("Модалка регистрации закрыта.")
        except Exception: pass
        # 1. Кликаем по первой ссылке в списке новостей
        # Метод click_first_news_list_item сам проверяет, что в списке есть элементы и кликает первую.
        print("Кликаем по первой ссылке новости в списке...")
        home_page.click_first_news_list_item()
        # --- Ассерт: Ожидаем и проверяем Навигацию в ТЕКУЩЕМ окне ---
        # Ожидаемый формат URL страницы новости: https://kaliningrad.hh.ru/article/ID...
        # Проверяем путь URL и что он начинается с "/article/".
        expected_url_path_prefix = "/article/"
        print(f"Ожидаем навигацию на путь URL, начинающийся с '{expected_url_path_prefix}'...")
        try:
            # wait_for_url ждет навигации в текущем окне на URL, который соответствует шаблону.
            page.wait_for_url(re.compile(rf"**{expected_url_path_prefix}\d+"), timeout=settings.NAVIGATION_TIMEOUT) 
            print(f"Страница новости (путь начинается с '{expected_url_path_prefix}' и содержит ID) достигнута.")
        except Exception as e:
             print(f"Ошибка ожидания навигации: {e}")
             assert False, f"Не удалось перейти на ожидаемую страницу новости. Текущий URL: {page.url}"
        # Дополнительно можно проверить, что URL содержит числовой ID после "/article/"
        current_url = page.url
        parsed_url = urlparse(current_url)
        assert parsed_url.path.startswith(expected_url_path_prefix)
        article_id = parsed_url.path.replace(expected_url_path_prefix, "")
        assert article_id.isdigit(), f"ID новости в URL '{article_id}' не является числовым."
        print("URL страницы новости корректен (путь начинается с '/article/' и содержит числовой ID).")
        print("Тест test_first_news_link_redirect завершен успешно.")

    # @pytest.mark.skip
    def test_articles_title_link_redirect(self, page: Page):
        """
        Проверяет видимость ссылки заголовка "Статьи" на главной странице
        и что клик по ней перенаправляет на страницу блога сайта в том же окне,
        и что на странице назначения присутствует ожидаемый заголовок "Блог".
        """
        home_page = HomePage(page)
        home_page.open()
        try: home_page.click_region_ok_button(); print("Модалка региона закрыта.")
        except Exception: pass
        try: expect(home_page.registration_modal_title).not_to_be_visible(timeout=10000); print("Модалка регистрации закрыта.")
        except Exception: pass
        # 1. Проверяем видимость и кликабельность ссылки заголовка на ГЛАВНОЙ СТРАНИЦЕ
        expect(home_page.articles_title_link).to_be_visible()
        expect(home_page.articles_title_link).to_be_enabled()
        print("Ссылка заголовка 'Статьи' на главной странице видна и доступна.")
        # 2. Кликаем по ссылке и ожидаем навигацию на страницу блога
        print("Кликаем по ссылке заголовка 'Статьи' и ожидаем навигацию на страницу блога...")
        home_page.click_articles_title_link()
        # --- Ассерт: Ожидаем и проверяем Навигацию в ТЕКУЩЕМ окне ---
        expected_url = "https://kaliningrad.hh.ru/articles?hhtmFrom=main"
        print(f"Ожидаем навигацию на URL: {expected_url}")
        try:
            page.wait_for_url(expected_url, timeout=settings.NAVIGATION_TIMEOUT)
            print(f"Страница навигации ({expected_url}) достигнута.")
        except Exception as e:
             print(f"Ошибка ожидания навигации: {e}")
             assert False, f"Не удалось перейти на ожидаемую страницу блога после клика по ссылке заголовка. Текущий URL: {page.url}"
        # 3. Проверяем наличие ключевого элемента НА СТРАНИЦЕ БЛОГА (/articles)
        expect(home_page.articles_site_blog_heading).to_be_visible(timeout=10000)
        print("На странице назначения (блог) найден ожидаемый заголовок 'Блог'.")
        # Можно также проверить наличие других элементов на странице блога
        check_element = page.getByText("СоискателямПредпринимателямРаботодателямСтудентамПутеводитель по компаниям", exact=True)
        expect(check_element).to_be_visible(timeout=10000)
        print("Тест test_articles_title_link_redirect завершен успешно.")

    # @pytest.mark.skip
    def test_articles_list_presence_and_count(self, page: Page):
        """
        Проверяет видимость контейнера списка статей и наличие в нем элементов (ссылок).
        """
        home_page = HomePage(page)
        home_page.open()
        try: home_page.click_region_ok_button(); print("Модалка региона закрыта.")
        except Exception: pass
        try: expect(home_page.registration_modal_title).not_to_be_visible(timeout=10000); print("Модалка регистрации закрыта.")
        except Exception: pass
        # 1. Проверяем видимость контейнера списка статей
        expect(home_page.articles_block_container).to_be_visible(timeout=10000) # Проверяем видимость всего блока статей
        expect(home_page.articles_list_container).to_be_visible(timeout=10000) # Проверяем видимость самого списка ul
        print("Контейнер списка статей 'Статьи' виден.")
        # 2. Проверяем наличие элементов (ссылок статей) в списке
        expect(home_page.articles_item_links).to_have_count(lambda count: count > 0, timeout=10000) 
        # oжидаем минимум 3 элемента:
        expect(home_page.articles_item_links).to_have_count(lambda count: count >= 3, timeout=10000)
        print(f"В списке статей найдено {home_page.articles_item_links.count()} элементов.")

    # @pytest.mark.skip
    def test_articles_sample_links_presence_and_href(self, page: Page):
        """
        Проверяет видимость первых нескольких ссылок в списке статей на главной странице и
        проверяет формат их URL (href).
        """
        home_page = HomePage(page)
        home_page.open()
        try: home_page.click_region_ok_button(); print("Модалка региона закрыта.")
        except Exception: pass
        try: expect(home_page.registration_modal_title).not_to_be_visible(timeout=10000); print("Модалка регистрации закрыта.")
        except Exception: pass
        # 1. Проверяем, что список статей виден и содержит достаточно элементов
        expect(home_page.articles_list_container).to_be_visible(timeout=10000)
        expected_min_count = 3
        expect(home_page.articles_item_links).to_have_count(lambda count: count >= expected_min_count, timeout=settings.DEFAULT_TIMEOUT) # Используем стандартный таймаут или больше
        print(f"Список статей виден и содержит минимум {expected_min_count} ссылок.")
        # 2. Проверяем видимость и формат URL (href) для первых N ссылок
        print(f"Проверяем видимость и URL первых {expected_min_count} ссылок в списке статей...")
        for i in range(expected_min_count):
            article_link = home_page.articles_item_links.nth(i)
            expect(article_link).to_be_visible() # Проверяем видимость
            # Проверяем формат URL (href). Ожидаем либо "/article/ID..." либо "https://my.hh.ru/..."
            href = article_link.get_attribute('href')
            print(f"Ссылка {i+1}: URL href = {href}")
            assert href is not None, f"Ссылка {i+1} не содержит атрибут href"
            # Проверяем, что href соответствует одному из ожидаемых шаблонов
            is_article_url = re.match(r"^/article/\d+", href) is not None # Начинается с /article/ и затем цифры
            is_my_hh_url = href.startswith("https://my.hh.ru/") # Начинается с https://my.hh.ru/
            assert is_article_url or is_my_hh_url, f"URL ссылки {i+1} ({href}) не соответствует ожидаемым форматам (/article/ID... или https://my.hh.ru/...)"
            print(f"Ссылка {i+1} видна и ее URL (href) корректен.")
        print("Тест test_articles_sample_links_presence_and_href завершен успешно.")

    # @pytest.mark.skip
    def test_useful_title_presence(self, page: Page):
        """
        Проверяет видимость и текст статического заголовка "Полезное".
        """
        home_page = HomePage(page)
        home_page.open()
        try: home_page.click_region_ok_button(); print("Модалка региона закрыта.")
        except Exception: pass
        try: expect(home_page.registration_modal_title).not_to_be_visible(timeout=10000); print("Модалка регистрации закрыта.")
        except Exception: pass
        # Проверяем видимость и текст заголовка
        expect(home_page.useful_title).to_be_visible()
        expect(home_page.useful_title).to_have_text("Полезное")
        print("Заголовок 'Полезное' виден и текст корректен.")

    # @pytest.mark.skip
    def test_useful_list_presence_and_count(self, page: Page):
        """
        Проверяет видимость контейнера списка "Полезное" и наличие в нем элементов (ссылок).
        """
        home_page = HomePage(page)
        home_page.open()
        try: home_page.click_region_ok_button(); print("Модалка региона закрыта.")
        except Exception: pass
        try: expect(home_page.registration_modal_title).not_to_be_visible(timeout=10000); print("Модалка регистрации закрыта.")
        except Exception: pass
        # 1. Проверяем видимость контейнера списка "Полезное"
        expect(home_page.useful_block_container).to_be_visible(timeout=10000) # Проверяем видимость всего блока
        expect(home_page.useful_list_container).to_be_visible(timeout=10000) # Проверяем видимость самого списка ul
        print("Контейнер списка 'Полезное' виден.")
        # 2. Проверяем наличие элементов (полезных ссылок) в списке
        # Локатор useful_item_links ищет все ссылки внутри списка ul.
        # Ожидаем, что в списке будет хотя бы 1 элемент (ссылка)
        expect(home_page.useful_item_links).to_have_count(lambda count: count > 0, timeout=10000)
        # Согласно HTML, ожидаем минимум 9 элементов:
        expect(home_page.useful_item_links).to_have_count(lambda count: count >= 9, timeout=10000)
        print(f"В списке 'Полезное' найдено {home_page.useful_item_links.count()} элементов.")

    # @pytest.mark.skip
    def test_first_useful_link_redirect(self, page: Page):
        """
        Находит первую полезную ссылку в списке "Полезное",
        кликает по ней и проверяет, что происходит перенаправление на страницу поиска вакансий
        с ожидаемым форматом URL (/vacancies/job_title).
        """
        home_page = HomePage(page)
        home_page.open()
        try: home_page.click_region_ok_button(); print("Модалка региона закрыта.")
        except Exception: pass
        try: expect(home_page.registration_modal_title).not_to_be_visible(timeout=10000); print("Модалка регистрации закрыта.")
        except Exception: pass
        # 1. Кликаем по первой ссылке в списке "Полезное"
        # Метод click_first_useful_list_item сам проверяет, что в списке есть элементы и кликает первую.
        print("Кликаем по первой полезной ссылке в списке 'Полезное'...")
        home_page.click_first_useful_list_item()
        # --- Ассерт: Ожидаем и проверяем Навигацию в ТЕКУЩЕМ окне ---
        # Ожидаемый формат URL страницы поиска: https://kaliningrad.hh.ru/vacancies/job_title
        # Проверяем путь URL и что он начинается с "/vacancies/".
        expected_url_path_prefix = "/vacancies/"
        print(f"Ожидаем навигацию на путь URL, начинающийся с '{expected_url_path_prefix}'...")
        try:
            # wait_for_url ждет навигации в текущем окне на URL, который соответствует шаблону.
            # Ожидаем путь /vacancies/ и что-то после (название профессии)
            page.wait_for_url(re.compile(rf"**{expected_url_path_prefix}.+"), timeout=settings.NAVIGATION_TIMEOUT)
            print(f"Страница поиска вакансий (путь начинается с '{expected_url_path_prefix}' и содержит название) достигнута.")
        except Exception as e:
             print(f"Ошибка ожидания навигации: {e}")
             assert False, f"Не удалось перейти на ожидаемую страницу поиска вакансий. Текущий URL: {page.url}"
        # Дополнительно можно проверить, что URL содержит непустой текст после "/vacancies/"
        current_url = page.url
        parsed_url = urlparse(current_url)
        job_title_slug = parsed_url.path.replace(expected_url_path_prefix, "")
        assert len(job_title_slug) > 0, f"URL страницы поиска содержит пустую строку после '{expected_url_path_prefix}'."
        print("URL страницы поиска вакансий корректен (путь начинается с '/vacancies/' и содержит название).")
        print("Тест test_first_useful_link_redirect завершен успешно.")

    # @pytest.mark.skip
    def test_other_cities_title_presence(self, page: Page):
        """
        Проверяет видимость и текст статического заголовка "Работа в других городах".
        """
        home_page = HomePage(page)
        home_page.open()
        try: home_page.click_region_ok_button(); print("Модалка региона закрыта.")
        except Exception: pass
        try: expect(home_page.registration_modal_title).not_to_be_visible(timeout=10000); print("Модалка регистрации закрыта.")
        except Exception: pass
        # Проверяем видимость и текст заголовка
        expect(home_page.other_cities_title).to_be_visible()
        expect(home_page.other_cities_title).to_have_text("Работа в других городах")
        print("Заголовок 'Работа в других городах' виден и текст корректен.")

    # @pytest.mark.skip
    def test_other_cities_list_presence_and_count(self, page: Page):
        """
        Проверяет видимость контейнера списка городов "Работа в других городах"
        и наличие в нем элементов (ссылок).
        """
        home_page = HomePage(page)
        home_page.open()
        try: home_page.click_region_ok_button(); print("Модалка региона закрыта.")
        except Exception: pass
        try: expect(home_page.registration_modal_title).not_to_be_visible(timeout=10000); print("Модалка регистрации закрыта.")
        except Exception: pass
        # 1. Проверяем видимость контейнера списка городов
        expect(home_page.other_cities_block_container).to_be_visible(timeout=10000) # Проверяем видимость всего блока
        expect(home_page.other_cities_list_container).to_be_visible(timeout=10000) # Проверяем видимость самого списка ul
        print("Контейнер списка городов 'Работа в других городах' виден.")
        # 2. Проверяем наличие элементов (ссылок городов) в списке
        # Локатор other_cities_item_links ищет все ссылки внутри списка ul.
        # Ожидаем, что в списке будет хотя бы 1 элемент (ссылка)
        expect(home_page.other_cities_item_links).to_have_count(lambda count: count > 0, timeout=10000)
        # Согласно HTML, ожидаем минимум 10 элементов:
        expect(home_page.other_cities_item_links).to_have_count(lambda count: count >= 10, timeout=10000)
        print(f"В списке 'Работа в других городах' найдено {home_page.other_cities_item_links.count()} элементов.")

    # @pytest.mark.skip
    def test_first_other_city_link_redirect(self, page: Page):
        """
        Находит первую ссылку города в списке "Работа в других городах",
        кликает по ней и проверяет, что происходит перенаправление на страницу
        с ожидаемым форматом hostname (subdomain.hh.ru).

        ВНИМАНИЕ: Дополнительные проверки на ТОЧНЫЙ URL https://gurievsk-kaliningrad.hh.ru/
        и наличие элемента get_by_role("button", name="Гурьевск (Калининградская область)")
        делают тест ХРУПКИМ, т.к. первый город в списке может меняться.
        Более надежный тест проверял бы только формат hostname '*.hh.ru'
        и общий элемент страницы города (например, заголовок 'Работа в [Название города]').
        """
        home_page = HomePage(page)
        home_page.open()
        try: home_page.click_region_ok_button(); print("Модалка региона закрыта.")
        except Exception: pass
        try: expect(home_page.registration_modal_title).not_to_be_visible(timeout=10000); print("Модалка регистрации закрыта.")
        except Exception: pass
        # 1. Кликаем по первой ссылке в списке городов
        # Метод click_first_other_cities_list_item сам проверяет, что в списке есть элементы и кликает первую.
        print("Кликаем по первой ссылке города в списке 'Работа в других городах'...")
        home_page.click_first_other_cities_list_item()
        # --- Ассерт: Ожидаем и проверяем Навигацию в ТЕКУЩЕМ окне ---
        # ВНИМАНИЕ: Эта проверка на КОНКРЕТНЫЙ URL делает тест ХРУПКИМ.
        # Она сработает, только если первый город - именно Гурьевск и URL точно такой.
        expected_exact_url = "https://gurievsk-kaliningrad.hh.ru/"
        print(f"Ожидаем навигацию на ТОЧНЫЙ URL: {expected_exact_url}")
        try:
            # wait_for_url ждет навигации в текущем окне на точный URL.
            page.wait_for_url(expected_exact_url, timeout=settings.NAVIGATION_TIMEOUT)
            print(f"Страница навигации ({expected_exact_url}) достигнута.")
        except Exception as e:
             print(f"Ошибка ожидания навигации на ТОЧНЫЙ URL: {e}")
             # В случае ошибки, выводим текущий URL для отладки
             print(f"Текущий URL после клика: {page.url}")
             assert False, f"Не удалось перейти на ожидаемую страницу города '{expected_exact_url}' после клика по первой ссылке. Возможно, первый город в списке изменился. Текущий URL: {page.url}"
        # 2. ВНИМАНИЕ: Эта проверка наличия КОНКРЕТНОГО элемента также делает тест ХРУПКИМ.
        # Локатор предоставлен пользователем для страницы Гурьевска.
        gurievsk_button_on_target_page = page.get_by_role("button", name="Гурьевск (Калининградская область)")
        # Проверяем видимость конкретной кнопки города на странице назначения
        print("Проверяем наличие кнопки 'Гурьевск (Калининградская область)' на странице...")
        expect(gurievsk_button_on_target_page).to_be_visible(timeout=10000)
        print("Кнопка 'Гурьевск (Калининградская область)' найдена на странице.")
        print("Тест test_first_other_city_link_redirect завершен успешно.")
        # page.pause()