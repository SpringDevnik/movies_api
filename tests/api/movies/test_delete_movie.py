import allure

from core.asserters.common_asserters import is_status_code_200
from fixtures.models.movies.user_context import UserContext
from helpers.db.movies_db_helper import MoviesDbHelper


@allure.epic("movie")
@allure.feature("Удаление фильма")
class TestDeleteMovie:

    @allure.story("Успешное удаление фильма")
    @allure.description("Удаление фильма")
    @allure.label("owner", "Andrey")
    def test_delete_exist_movie(
        self,
        f_super_admin_ctx: UserContext,
        s_movie_db_helper: MoviesDbHelper,
        f_existed_movie_id: int,
    ) -> None:
        response, raw_response = f_super_admin_ctx.api_manager.movies.delete_movie(f_existed_movie_id).as_tuple()
        is_status_code_200(raw_response)
        # TODO добавить ассерты респонса и факта удаления записи о фильме
