from typing import Self, override

from pydantic import Field

from core.asserters.common_asserters import equal
from core.pydantic.annotations.type import NonBlankStr, NonNegativeInt
from core.pydantic.models.base_http_models import RequestBaseModel, ResponseBaseModel
from core.utils.fake import faker, generate_password
from enums.auth.user_roles import UserRole


class LoginRequest(RequestBaseModel):
    email: NonBlankStr | None = Field(default_factory=faker.email)
    password: NonBlankStr | None = Field(default_factory=generate_password)


class _User(ResponseBaseModel):
    id: NonBlankStr
    email: NonBlankStr
    full_name: NonBlankStr
    roles: list[UserRole] = Field(..., min_length=1)

    @override
    def match(self, expected: Self) -> None:
        equal(self.id, expected.id, "id")
        equal(self.email, expected.email, "email")
        equal(self.full_name, expected.full_name, "full_name")
        equal(self.roles, expected.roles, "roles")


class LoginResponse(ResponseBaseModel):
    user: _User
    access_token: NonBlankStr
    refresh_token: NonBlankStr
    expiresIn: NonNegativeInt

    @override
    def match(self, expected: Self) -> None:
        self.user.match(expected.user)
