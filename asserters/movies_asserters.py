import allure
import requests

from api.api_manager import ApiManager
from core.asserters.common_asserters import contains_all
from models.api.user import Credentials
from _settings import settings
from models.api.movies.common.genre import Genre


@allure.step("Проверка существования жанра")
def assert_genre_exist(genre_name: str) -> None:
    session = requests.Session()
    api_manager = ApiManager(session=session, base_headers=settings.api.BASE_HEADERS)
    creds = Credentials(
        email=settings.api.SUPER_ADMIN_LOGIN,
        password=settings.api.SUPER_ADMIN_PASSWORD,
    )
    api_manager.auth.authenticate(creds)
    response = api_manager.movies.get_genres_list().response
    contains_all(
        container=response.root,
        elements=[Genre(name=genre_name)],
    )
