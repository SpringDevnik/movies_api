from typing import Self

from core.asserters.common_asserters import equal
from core.pydantic.models.base_http_models import ResponseBaseRootModel
from models.api.movies.common.genre import Genre


class GetGenresListResponse(ResponseBaseRootModel[list[Genre]]):
    def match(self, expected: Self) -> None:
        equal(self.root, expected.root, "list[Genre]")
