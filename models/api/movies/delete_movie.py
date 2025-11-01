from datetime import datetime
from typing import Self, override

from pydantic import Field

from core.asserters.common_asserters import equal, is_positive_num
from core.pydantic.annotations.type import NonBlankStr, PositiveInt, NonNegativeInt
from core.pydantic.models.base_http_models import ResponseBaseModel
from enums.movie.locations import Location
from models.api.movies.common.genre import Genre
from models.api.movies.common.review import Review


class DeleteMovieResponse(ResponseBaseModel):
    id: PositiveInt = Field(..., gt=0)
    name: NonBlankStr
    price: NonNegativeInt = Field(..., gt=0)
    description: NonBlankStr
    image_url: NonBlankStr
    location: Location
    published: bool
    genre_id: PositiveInt = Field(..., gt=0)
    genre: Genre
    created_at: datetime
    reviews: list[Review]
    rating: NonNegativeInt = Field(..., ge=0)

    @override
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
        equal(self.reviews, expected.reviews, "reviews")
