from datetime import datetime
from typing import Self, override

from pydantic import Field

from core.asserters.common_asserters import compare_dates, equal
from core.pydantic.annotations.type import NonBlankStr
from core.pydantic.models.base_http_models import ResponseBaseModel
from enums.auth.user_roles import UserRole


class GetUserInfoResponse(ResponseBaseModel):
    id: NonBlankStr
    email: NonBlankStr
    full_name: NonBlankStr
    roles: list[UserRole] = Field(..., min_length=1)
    verified: bool
    created_at: datetime
    banned: bool

    @override
    def match(self, expected: Self) -> None:
        equal(self.id, expected.id, "id")
        equal(self.email, expected.email, "email")
        equal(self.full_name, expected.full_name, "full_name")
        equal(self.roles, expected.roles, "roles")
        equal(self.verified, expected.verified, "verified")
        compare_dates(self.created_at, expected.created_at, prefix="created_at")
        equal(self.banned, expected.banned, "banned")
