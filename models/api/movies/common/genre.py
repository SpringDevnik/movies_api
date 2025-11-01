from typing import Self, override

from core.asserters.common_asserters import equal
from core.pydantic.annotations.type import NonBlankStr
from core.pydantic.models.base_http_models import ResponseBaseModel


class Genre(ResponseBaseModel):
    name: NonBlankStr

    @override
    def match(self, expected: Self) -> None:
        if expected.name != "UNPREDICTABLE":
            equal(self.name, expected.name, "name")
