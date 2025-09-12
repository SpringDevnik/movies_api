from abc import ABC, abstractmethod


class BaseHttpClient(ABC):

    @abstractmethod
    def __init__(self, base_url, base_headers):
        """
        Инициализация клиента.
        :param base_url: Базовый URL API.
        :param base_headers: Словарь базовых заголовков.
        """
        self.base_url = base_url
        self.headers = base_headers.copy()

    @abstractmethod
    def send_request(
            self,
            method,
            endpoint,
            data=None,
            expected_status=200,
            need_logging=True,
    ):
        pass
