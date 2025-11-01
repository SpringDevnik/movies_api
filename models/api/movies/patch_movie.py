from datetime import datetime
from typing import Self

from core.asserters.common_asserters import equal, is_positive_num
from core.pydantic.annotations.type import NonBlankStr, NonNegativeInt
from core.pydantic.models.base_http_models import RequestBaseModel, ResponseBaseModel
from enums.movie.locations import Location
from models.api.movies.common.genre import Genre


class PatchMovieRequest(RequestBaseModel):
    name: str | None = None
    image_url: str | None = None
    price: int | None = None
    description: str | None = None
    location: Location | None = None
    published: bool | None = None
    genre_id: int | None = None


class PatchMovieResponse(ResponseBaseModel):
    id: NonNegativeInt
    name: NonBlankStr
    price: NonNegativeInt
    description: NonBlankStr
    image_url: NonBlankStr
    location: Location
    published: bool
    genre_id: NonNegativeInt
    genre: Genre
    created_at: datetime
    rating: NonNegativeInt

    def match(self, expected: Self) -> None:
        is_positive_num(self.id)
        equal(self.name, expected.name, "name")
        equal(self.price, expected.price, "price")
        equal(self.description, expected.description, "description")
        equal(self.image_url, expected.image_url, "image_url")
        equal(self.location, expected.location, "location")
        equal(self.published, expected.published, "published")
        equal(self.genre_id, expected.genre_id, "genre_id")
        # TODO подумать о рекурсивной проверки внутри моделей
        self.genre.match(expected.genre)
        # TODO узнать часовой пояс сервера
        # assert_equal(self.created_at, expected.created_at)
        equal(self.rating, expected.rating, "rating")
