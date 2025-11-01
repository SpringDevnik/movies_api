import allure
import pytest
from sqlalchemy.orm import Session

from fixtures.models.common.movie_data import MovieData
from fixtures.models.movies.user_context import UserContext
from helpers.db.movies_db_helper import MoviesDbHelper
from models.api.movies.create_movie import CreateMovieRequest


@allure.title("Получение MovieDbHelper")
@pytest.fixture(scope="session")
def s_movie_db_helper(s_db_session: Session) -> MoviesDbHelper:
    return MoviesDbHelper(s_db_session)


@allure.title("Получение фейковых данных о фильме")
@pytest.fixture
def f_random_movie_data() -> MovieData:
    return MovieData()


@allure.title("Получение фейковых данных о фильме")
@pytest.fixture
def f_existed_movie_id(f_super_admin_ctx: UserContext, s_movie_db_helper: MoviesDbHelper) -> int:
    genre = s_movie_db_helper.get_random_genre()
    request = CreateMovieRequest(genre_id=genre.id)
    response = f_super_admin_ctx.api_manager.movies.create_movie(request).response
    return response.id
    # TODO подумать о механизме очистки созданных фильмов
