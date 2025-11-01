from typing import Iterator

import allure
import pytest
import requests
from sqlalchemy.orm import Session

from api.api_manager import ApiManager
from core.db.sqlalchemy.postgres.pg_client import PgClient
from enums.auth.user_roles import UserRole
from fixtures.models.movies.user_context import UserContext
from models.api.user import User, Credentials
from _settings import settings


@allure.title("Получение Postgres сессии")
@pytest.fixture(scope="session")
def s_db_session(s_pg_client: PgClient) -> Iterator[Session]:
    session: Session = s_pg_client.get_new_db_session()
    yield session
    session.rollback()
    session.close()


@allure.title("Получение Postgres сессии")
@pytest.fixture(scope="session")
def s_pg_client() -> PgClient:
    return PgClient(
        host=settings.db.DB_HOST,
        database_name=settings.db.DB_NAME,
        port=settings.db.DB_PORT,
        username=settings.db.DB_USERNAME.get_secret_value(),
        password=settings.db.DB_PASSWORD.get_secret_value(),
    )


@allure.title("Получение контекста супер админа")
@pytest.fixture
def f_super_admin_ctx(f_api_manager: ApiManager) -> UserContext:
    super_admin = User(
        email=settings.api.SUPER_ADMIN_LOGIN.get_secret_value(),
        password=settings.api.SUPER_ADMIN_PASSWORD.get_secret_value(),
        roles=[UserRole.SUPER_ADMIN],
    )
    creds = Credentials(
        email=super_admin.email,
        password=super_admin.password,
    )
    f_api_manager.auth.authenticate(creds)
    return UserContext(super_admin, f_api_manager)


@allure.title("Получение requests сессии")
@pytest.fixture(scope="session")
def s_session() -> Iterator[requests.Session]:
    session = requests.Session()

    yield session

    session.close()


@allure.title("Получение requests сессии")
@pytest.fixture
def f_session() -> Iterator[requests.Session]:
    session = requests.Session()

    yield session

    session.close()


@allure.title("Получение ApiManager")
@pytest.fixture
def f_api_manager(s_session: requests.Session, request: pytest.FixtureRequest) -> ApiManager:
    item_logger = None
    if hasattr(request.node, "test_logger"):
        item_logger = request.node.test_logger

    return ApiManager(
        base_headers=settings.api.BASE_HEADERS,
        session=s_session,
        logger=item_logger,
    )
