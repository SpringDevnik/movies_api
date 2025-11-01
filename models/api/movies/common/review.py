from datetime import datetime
from typing import Self, override

from core.asserters.common_asserters import equal
from core.pydantic.annotations.type import NonBlankStr, PositiveInt
from core.pydantic.models.base_http_models import ResponseBaseModel


class User(ResponseBaseModel):
    full_name: NonBlankStr

    @override
    def match(self, expected: Self) -> None:
        if expected.full_name != "UNPREDICTABLE":
            equal(self.full_name, expected.full_name, "full_name")


class Review(ResponseBaseModel):
    user_id: NonBlankStr
    rating: PositiveInt
    text: NonBlankStr
    created_at: datetime
    user: User

    @override
    def match(self, expected: Self) -> None:
        equal(self.user_id, expected.user_id, "user_id")
        equal(self.rating, expected.rating, "rating")
        equal(self.text, expected.text, "text")
        equal(self.created_at, expected.created_at, "created_at")
        equal(self.user, expected.user, "user")
