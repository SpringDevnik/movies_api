import requests

from constants import AUTH_API_BASE_URL, BASE_HEADERS
from core.http_client import HttpClient
from enums.auth.endpoints import Endpoint


class AuthApi(HttpClient):
    """
    Класс для работы с аутентификацией.
    """

    def __init__(
            self,
            session=None,
            base_url=AUTH_API_BASE_URL,
            base_headers=BASE_HEADERS,
    ):
        session_ = requests.Session() if session is None else session
        super().__init__(session_, base_url, base_headers)

    def register_user(self, user_data, expected_status=201):
        """
       Регистрация нового пользователя.
       :param user_data: Данные пользователя.
       :param expected_status: Ожидаемый статус-код.
       """
        return self.send_request(
            method="POST",
            endpoint=Endpoint.REGISTER.value,
            data=user_data,
            expected_status=expected_status,
        )

    def login_user(self, login_data, expected_status=200):
        """
        Авторизация пользователя.
        :param login_data: Данные для логина.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="POST",
            endpoint=Endpoint.LOGIN.value,
            data=login_data,
            expected_status=expected_status,
        )

    def authenticate(self, user_creds):
        login_data = {
            "email": user_creds[0],
            "password": user_creds[1]
        }

        response = self.login_user(login_data).json()
        if "accessToken" not in response:
            raise KeyError("token is missing")

        token = response["accessToken"]
        self._update_session_headers(**{"authorization": "Bearer " + token})
