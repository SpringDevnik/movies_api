import allure

from api.auth_api import AuthApi
from core.asserters.common_asserters import is_status_code_200
from fixtures.models.auth.user_data import UserData
from models.api.auth.login_user import LoginRequest, LoginResponse, _User


@allure.epic("auth")
@allure.feature("Авторизация пользователя")
class TestLogin:

    @allure.story("Успешная авторизация пользователя")
    @allure.description("Авторизация зарегистрированного пользователя")
    @allure.label("owner", "Andrey")
    def test_login_registered_user(
        self,
        s_auth_api: AuthApi,
        f_registered_user_data: UserData,
    ) -> None:
        """
        Тест на регистрацию и авторизацию пользователя.
        """
        request = LoginRequest(
            email=f_registered_user_data.email,
            password=f_registered_user_data.password,
        )
        expected_response = LoginResponse(
            user=_User(
                id=f_registered_user_data.id,
                email=f_registered_user_data.email,
                full_name=f_registered_user_data.full_name,
                roles=f_registered_user_data.roles,
            ),
            access_token="unpredictable",
            refresh_token="unpredictable",
            expiresIn=-1,  # unpredictable
        )

        response, raw_response = s_auth_api.login_user(request).as_tuple()

        is_status_code_200(raw_response)
        response.match(expected_response)
