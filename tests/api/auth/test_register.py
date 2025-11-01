import datetime

import allure

from api.auth_api import AuthApi
from core.asserters.common_asserters import is_status_code
from core.utils.fake import generate_password
from enums.auth.user_roles import UserRole
from models.api.auth.register_user import RegisterRequest, RegisterResponse


@allure.epic("auth")
@allure.feature("Регистрация пользователя")
class TestRegister:

    @allure.story("Успешная регистрация пользователя")
    @allure.description("Регистрация нового пользователя")
    @allure.label("owner", "Andrey")
    def test_register_user(self, s_auth_api: AuthApi) -> None:
        password = generate_password()
        request = RegisterRequest(
            password=password,
            password_repeat=password,
        )
        expected_response = RegisterResponse(
            id="unpredictable",
            email=request.email,
            full_name=request.full_name,
            roles=[UserRole.USER],
            banned=False,
            verified=True,
            created_at=datetime.datetime.now(),  # unpredictable
        )

        response_model, response = s_auth_api.register_user(request).as_tuple()

        is_status_code(201, response)
        response_model.match(expected_response)
