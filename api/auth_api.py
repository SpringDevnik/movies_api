import logging
from typing import Annotated, Mapping

import allure
from requests import Session

from core.http.requests.http_client import HttpClient
from core.pydantic.models.response_wrapper import HttpResponseWrapper
from enums.auth.endpoints import Endpoint
from models.api.auth.create_user import CreateUserRequest, CreateUserResponse
from models.api.auth.get_user_info import GetUserInfoResponse
from models.api.auth.login_user import LoginRequest, LoginResponse
from models.api.auth.register_user import RegisterRequest, RegisterResponse
from models.api.user import Credentials
from settings import settings

IdOrEmail = Annotated[str, "UUID or Email"]


class AuthApi(HttpClient):
    """
    Класс для работы с аутентификацией.
    """

    def __init__(
        self,
        *,
        base_headers: Mapping[str, str] = settings.api.BASE_HEADERS,
        base_url: str = settings.api.AUTH_API_BASE_URL,
        session: Session | None = None,
        logger: logging.Logger | None = None,
    ):
        super().__init__(
            base_headers=base_headers,
            session=session,
            base_url=base_url,
            logger=logger,
        )

    @allure.step("Зарегистрировать пользователя")
    def register_user(
        self,
        request: RegisterRequest,
    ) -> HttpResponseWrapper[RegisterResponse]:
        """
        Регистрация нового пользователя.
        :param request: Данные запроса на регистрацию.
        """
        return self.post(
            endpoint=str(Endpoint.REGISTER),
            json=request.model_dump(by_alias=True),
            response_model=RegisterResponse,
        )

    @allure.step("Авторизовать пользователя")
    def login_user(
        self,
        request: LoginRequest,
    ) -> HttpResponseWrapper[LoginResponse]:
        """
        Авторизация пользователя.
        :param request: Данные для логина.
        """
        return self.post(
            endpoint=str(Endpoint.LOGIN),
            json=request.model_dump(by_alias=True),
            response_model=LoginResponse,
        )

    @allure.step("Создать нового пользователя")
    def create_user(
        self,
        request: CreateUserRequest,
    ) -> HttpResponseWrapper[CreateUserResponse]:
        return self.post(
            endpoint=str(Endpoint.USER),
            json=request.model_dump(by_alias=True),
            response_model=CreateUserResponse,
        )

    @allure.step("Получить информацию о пользователе")
    def get_user(
        self,
        locator: IdOrEmail,
    ) -> HttpResponseWrapper[GetUserInfoResponse]:
        return self.get(
            endpoint=f"{Endpoint.USER.value}/{locator}",
            response_model=GetUserInfoResponse,
        )

    # todo Под вопросом
    def authenticate(self, user_creds: Credentials) -> None:
        login_request = LoginRequest(
            email=user_creds.email,
            password=user_creds.password,
        )
        access_token = self.login_user(login_request).response.access_token
        self._update_session_headers(authorization=f"Bearer {access_token}")
