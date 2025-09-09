import requests
from faker import Faker
import pytest

from api.api_manager import ApiManager
from api.auth_api import AuthApi
from api.movie_api import MoviesApi
from constants import BASE_HEADERS, SUPER_ADMIN_CREDS
from api.dto.genre import Genre
from enums.auth.endpoints import Endpoint
from enums.auth.password_rules import PasswordRule
from enums.movie.locations import Location

faker = Faker()


@pytest.fixture(scope="session")
def random_user():
    password_length = faker.random_int(
        min=PasswordRule.MIN_LENGTH.value,
        max=PasswordRule.MAX_LENGTH.value,
    )
    password = faker.password(
        length=password_length,
        special_chars=PasswordRule.HAS_SPECIAL_CHAR.value,
        digits=PasswordRule.HAS_DIGIT.value,
        upper_case=PasswordRule.HAS_UPPERCASE.value,
        lower_case=PasswordRule.HAS_LOWERCASE.value,
    )
    return {
        "email": faker.email(),
        "fullName": faker.name(),
        "password": password,
        "passwordRepeat": password,
    }


@pytest.fixture
def auth_session(random_user, auth_api):
    auth_api.send_request(
        method="POST",
        endpoint=Endpoint.REGISTER.value,
        json=random_user,
        headers=BASE_HEADERS,
    )

    login_data = {
        "email": f"{random_user["email"]}",
        "password": f"{random_user["password"]}",
    }

    response = auth_api.send_request(
        method="POST",
        endpoint=Endpoint.LOGIN.value,
        json=login_data,
        headers=BASE_HEADERS,
    )
    token = response.json()["token"]

    session = requests.Session()
    session.headers.update(BASE_HEADERS)
    session.headers.update({"Authorization": f"Bearer {token}"})

    return session


@pytest.fixture(scope="session")
def registered_user(auth_api, random_user):
    """
    Фикстура для регистрации и получения данных зарегистрированного пользователя.
    """
    response = auth_api.send_request(
        method="POST",
        endpoint=Endpoint.REGISTER.value,
        data=random_user,
        expected_status=201,
    )
    response_data = response.json()
    registered_user = random_user.copy()
    registered_user["id"] = response_data["id"]
    return registered_user


@pytest.fixture(scope="session")
def auth_api():
    """
    Фикстура для создания экземпляра CustomRequester.
    """
    session = requests.Session()
    return AuthApi(session=session)


@pytest.fixture(scope="session")
def movies_api():
    """
    Фикстура для создания экземпляра CustomRequester.
    """
    session = requests.Session()
    return MoviesApi(session=session)


@pytest.fixture(scope="session")
def session():
    """
    Фикстура для создания HTTP-сессии.
    """
    http_session = requests.Session()
    yield http_session
    http_session.close()


@pytest.fixture(scope="session")
def api_manager(session):
    """
    Фикстура для создания экземпляра ApiManager.
    """
    return ApiManager(session)


@pytest.fixture
def random_movie_data():
    return {
        "name": " ".join(faker.words(nb=faker.random_int(1, 2))),
        "imageUrl": faker.url(),
        "price": faker.random_int(1, 10),
        "description": faker.text(max_nb_chars=100),
        "location": faker.random_element(list(Location)).value,
        "published": faker.boolean(),
        "genreId": faker.random_int(1, 10)
    }


@pytest.fixture(scope="session")
def super_admin_token(auth_api):
    login_data = {
        "email": SUPER_ADMIN_CREDS["login"],
        "password": SUPER_ADMIN_CREDS["password"],
    }

    response = auth_api.send_request(
        method="POST",
        endpoint=Endpoint.LOGIN.value,
        data=login_data,
    )
    return response.json()["accessToken"]
