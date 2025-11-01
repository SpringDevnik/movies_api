from datetime import datetime
from typing import Self, override

from pydantic import Field

from core.asserters.common_asserters import equal
from core.pydantic.annotations.type import NonBlankStr
from core.pydantic.models.base_http_models import RequestBaseModel, ResponseBaseModel
from core.utils.fake import faker, generate_password
from enums.auth.user_roles import UserRole


class CreateUserRequest(RequestBaseModel):
    full_name: NonBlankStr | None = Field(default_factory=faker.name)
    email: NonBlankStr | None = Field(default_factory=faker.email)
    password: NonBlankStr | None = Field(default_factory=generate_password)
    verified: bool | None = Field(default_factory=faker.boolean)
    banned: bool | None = Field(default_factory=faker.boolean)


class CreateUserResponse(ResponseBaseModel):
    id: NonBlankStr
    email: NonBlankStr
    full_name: NonBlankStr
    roles: list[UserRole] = Field(..., min_length=1)
    verified: bool
    created_at: datetime
    banned: bool

    @override
    def match(self, expected: Self) -> None:
        equal(self.email, expected.email, "email")
        equal(self.full_name, expected.full_name, "full_name")
        equal(self.roles, expected.roles, "roles")
        equal(self.verified, expected.verified, "verified")
        # assert_date(self.created_at, expected.created_at)
        equal(self.banned, expected.banned, "banned")
