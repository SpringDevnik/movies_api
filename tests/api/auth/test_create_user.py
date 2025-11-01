import datetime
from typing import cast

import allure
import pytest

from core.asserters.common_asserters import is_status_code
from enums.auth.user_roles import UserRole
from fixtures.models.movies.user_context import UserContext
from models.api.auth.create_user import CreateUserRequest, CreateUserResponse


@allure.epic("auth")
@allure.feature("Создание пользователя")
class TestCreateUser:

    @allure.story("Успешное создание пользователя")
    @allure.description("Создание нового пользователя")
    @allure.label("owner", "Andrey")
    @pytest.mark.xfail(reason="Создается пользователь с флагом banned=True")
    def test_create_user(self, super_admin_ctx: UserContext) -> None:
        auth_api = super_admin_ctx.api_manager.auth
        request = CreateUserRequest()
        expected_response = CreateUserResponse(
            id="unpredictable",
            email=cast(str, request.email),
            full_name=cast(str, request.full_name),
            roles=[UserRole.USER],
            verified=True,
            created_at=datetime.datetime.now(),  # unpredictable
            banned=False,
        )
        response, raw_response = auth_api.create_user(request).as_tuple()

        is_status_code(201, raw_response)
        response.match(expected_response)
