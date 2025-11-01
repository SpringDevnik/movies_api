import allure

from core.asserters.common_asserters import is_status_code_200
from core.utils import fake
from fixtures.models.movies.user_context import UserContext
from helpers.db.movies_db_helper import MoviesDbHelper
from models.api.movies.patch_movie import PatchMovieRequest


@allure.epic("movie")
@allure.feature("Редактирование фильма")
class TestPathMovie:

    @allure.story("Успешное редактирование фильма")
    @allure.description("Редактирование названия фильма")
    @allure.label("owner", "Andrey")
    def test_patch_exist_movie(
        self,
        f_super_admin_ctx: UserContext,
        s_movie_db_helper: MoviesDbHelper,
        f_existed_movie_id: int,
    ) -> None:
        requests = PatchMovieRequest(name=fake.faker.name())
        response, raw_response = f_super_admin_ctx.api_manager.movies.patch_movie(
            movie_id=f_existed_movie_id,
            request=requests,
        ).as_tuple()
        is_status_code_200(raw_response)
        # TODO добавить ассерты респонса и факта обновленияо записи о фильме
