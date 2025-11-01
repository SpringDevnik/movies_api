import allure

from core.asserters.common_asserters import is_status_code_200
from fixtures.models.auth.user_data import UserData
from fixtures.models.movies.user_context import UserContext
from models.api.auth.get_user_info import GetUserInfoResponse


@allure.epic("auth")
@allure.feature("Получение информации о пользователе")
class TestGetUser:

    @allure.story("Успешное получение информации о пользователе")
    @allure.description("Получение информации о существующем пользователе по ID")
    @allure.label("owner", "Andrey")
    def test_get_user_by_id(
        self,
        f_super_admin_ctx: UserContext,
        f_registered_user_data: UserData,
    ) -> None:
        auth_api = f_super_admin_ctx.api_manager.auth
        expected_response = GetUserInfoResponse(
            **f_registered_user_data.model_dump(exclude={"password"}),
        ).model_copy(update={"banned": False})

        response, raw_response = auth_api.get_user(
            f_registered_user_data.id,
        ).as_tuple()

        is_status_code_200(raw_response)
        response.match(expected_response)
