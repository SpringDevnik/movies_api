from datetime import datetime
from typing import Self, override

from pydantic import Field

from core.asserters.common_asserters import equal
from core.pydantic.annotations.type import NonBlankStr
from core.pydantic.models.base_http_models import RequestBaseModel, ResponseBaseModel
from core.utils.fake import faker, generate_password
from enums.auth.user_roles import UserRole


class RegisterRequest(RequestBaseModel):
    email: NonBlankStr | None = Field(default_factory=lambda: faker.email().replace("_", ""))
    full_name: NonBlankStr | None = Field(default_factory=faker.name)
    password: NonBlankStr | None = Field(default_factory=generate_password)
    password_repeat: NonBlankStr | None = Field(default_factory=generate_password)


class RegisterResponse(ResponseBaseModel):
    id: NonBlankStr
    email: NonBlankStr
    full_name: NonBlankStr
    roles: list[UserRole] = Field(..., min_length=1)
    banned: bool
    verified: bool
    created_at: datetime

    @override
    def match(self, expected: Self) -> None:
        equal(self.email, expected.email, "email")
        equal(self.full_name, expected.full_name, "full_name")
        equal(self.roles, expected.roles, "roles")
        equal(self.banned, expected.banned, "banned")
        equal(self.verified, expected.verified, "verified")
        # assert_date(self.created_at, expected.created_at)
