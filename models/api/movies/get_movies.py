from datetime import datetime
from typing import Self, cast, override

from pydantic import Field

from core.asserters.common_asserters import equal
from core.pydantic.annotations.type import NonBlankStr, NonNegativeInt, PositiveInt
from core.pydantic.models.base_http_models import RequestBaseModel, ResponseBaseModel
from core.utils.fake import faker
from enums.movie.locations import Location
from enums.movie.sort_order import SortOrder
from models.api.movies.common.genre import Genre


class GetMoviesParams(RequestBaseModel):
    page_size: NonNegativeInt | None = Field(default_factory=lambda: faker.random_int(min=1))
    page: NonNegativeInt | None = Field(default_factory=lambda: faker.random_int(min=1))
    min_price: NonNegativeInt | None = Field(default_factory=lambda: faker.random_int(min=1))
    max_price: NonNegativeInt | None = Field(default_factory=lambda: faker.random_int(min=1))
    locations: list[Location] | None = Field(
        default_factory=lambda: cast(
            list,
            faker.random_choices(Location, length=len(Location)),
        ),
    )

    published: bool | None
    genre_id: PositiveInt | None = Field(default_factory=lambda: faker.random_int(min=1))
    create_at: NonBlankStr | None = Field(default_factory=lambda: faker.random_element(SortOrder))


class _Movie(ResponseBaseModel):
    id: PositiveInt = Field(..., gt=0)
    name: NonBlankStr
    description: NonBlankStr
    genre_id: PositiveInt = Field(..., gt=0)
    image_url: NonBlankStr
    price: NonNegativeInt = Field(..., gt=0)
    rating: NonNegativeInt = Field(..., ge=0)
    location: Location
    published: bool
    created_at: datetime
    genre: Genre

    @override
    def match(self, expected: Self) -> None:
        equal(self.id, expected.id, "id")
        equal(self.name, expected.name, "name")
        equal(self.description, expected.description, "description")
        equal(self.genre_id, expected.genre_id, "genre_id")
        equal(self.image_url, expected.image_url, "image_url")
        equal(self.price, expected.price, "price")
        equal(self.rating, expected.rating, "rating")
        equal(self.location, expected.location, "location")
        equal(self.published, expected.published, "published")
        equal(self.created_at, expected.created_at, "created_at")
        # TODO подумать о рекурсивной проверки внутри моделей
        self.genre.match(expected.genre)


class GetMoviesResponse(ResponseBaseModel):
    movies: list[_Movie]
    count: NonNegativeInt
    page: NonNegativeInt
    page_size: NonNegativeInt
    page_count: NonNegativeInt

    def match(self, expected: Self) -> None:
        equal(self.movies, expected.movies, "movies")
        equal(self.count, expected.count, "count")
        equal(self.page, expected.page, "page")
        equal(self.page_size, expected.page_size, "page_size")
        equal(self.page_count, expected.page_count, "page_count")
