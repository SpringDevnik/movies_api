from typing import Iterable

import allure
import pytest
import requests

from settings import settings
from api.auth_api import AuthApi
from api.movies_api import MoviesApi
from core.utils.fake import generate_password
from fixtures.models.auth.user_data import UserData
from models.api.auth.login_user import LoginRequest
from models.api.auth.register_user import RegisterRequest


@allure.title("Получение фейковых пользовательских данных")
@pytest.fixture
def f_user_data() -> UserData:
    return UserData()


@allure.title("Регистрация нового пользователя и получение его данных")
@pytest.fixture
def f_registered_user_data(s_auth_api: AuthApi) -> UserData:
    password = generate_password()
    request = RegisterRequest(
        password=password,
        password_repeat=password,
    )
    # TODO Возможно, стоит искать существующего пользака, а не регать нового каждый раз
    response = s_auth_api.register_user(request).response
    return UserData(**response.model_dump(), password=password)


@allure.title("Получение AuthApi")
@pytest.fixture(scope="session")
def s_auth_api(s_session: requests.Session) -> AuthApi:
    return AuthApi(session=s_session)


@allure.title("Получение MoviesApi")
@pytest.fixture(scope="session")
def s_movies_api(s_session: requests.Session) -> MoviesApi:
    return MoviesApi(session=s_session)


@allure.title("Регистрация пользователя и получение сессии с его auth кредами")
@pytest.fixture
def f_auth_session(s_auth_api: AuthApi) -> Iterable[requests.Session]:
    register_request = RegisterRequest()
    s_auth_api.register_user(register_request)

    login_request = LoginRequest(
        email=register_request.email,
        password=register_request.password,
    )
    access_token = s_auth_api.login_user(login_request).response.access_token

    session = requests.Session()
    session.headers.update(settings.api.BASE_HEADERS)
    session.headers.update({"Authorization": f"Bearer {access_token}"})

    yield session

    session.close()
