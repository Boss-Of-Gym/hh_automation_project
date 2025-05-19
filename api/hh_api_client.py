import requests
from config.settings import BASE_URL # Возможно, понадобится отдельный BASE_API_URL, но пока используем этот или вписываем явно

class HhApiClient:
    """Клиент для взаимодействия с API HH.ru."""

    def __init__(self):
        # API HH.ru имеет отдельный базовый URL, отличный от основного сайта
        self.base_api_url = "https://api.hh.ru/"
        self.session = requests.Session() # Использование сессии может быть полезно

    def _send_request(self, method, url, **kwargs):
        """Внутренний метод для отправки запросов."""
        full_url = f"{self.base_api_url}{url}"
        print(f"Отправка API запроса: {method.upper()} {full_url}") # Логирование запросов
        try:
            response = self.session.request(method, full_url, **kwargs)
            response.raise_for_status() # Выбросит исключение для плохих статусов (4xx или 5xx)
            print(f"Получен ответ: {response.status_code}") # Логирование ответа
            return response
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при выполнении API запроса: {e}")
            # В реальном проекте здесь может быть более сложная обработка ошибок или логирование
            raise # Перевыбрасываем исключение после логирования

    # Здесь будут добавляться методы для конкретных API эндпоинтов, например:
    # def search_vacancies(self, text, params=None):
    #     url = "vacancies"
    #     query_params = {"text": text}
    #     if params:
    #         query_params.update(params)
    #     response = self._send_request("GET", url, params=query_params)
    #     return response.json() # Возвращаем JSON-тело ответа

    # def get_vacancy_details(self, vacancy_id):
    #     url = f"vacancies/{vacancy_id}"
    #     response = self._send_request("GET", url)
    #     return response.json()