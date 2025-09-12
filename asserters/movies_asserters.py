import requests

from api.api_manager import ApiManager
from api.auth_api import AuthApi
from api.dto.genre import Genre
from api.movie_api import MoviesApi
from asserters.common_asserters import assert_list_contains_all
from constants import SUPER_ADMIN_CREDS


def assert_genre_exist(genreId: int, genreName: str):
    session = requests.Session()
    api_manager = ApiManager(session=session)
    login_data = {
        "email": SUPER_ADMIN_CREDS["login"],
        "password": SUPER_ADMIN_CREDS["password"]
    }
    access_token = api_manager.auth_api.login_user(
        login_data=login_data,
    ).json()["accessToken"]
    api_manager.session.headers.update(
        {"Authorization": f"Bearer {access_token}"},
    )
    actual_genres: list[Genre] = api_manager.movies_api.get_genres_list()
    assert_list_contains_all(
        container=actual_genres,
        sublist=[Genre(id=genreId, name=genreName)],
    )
