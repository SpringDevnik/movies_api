from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from core.pydantic.annotations.type import NonBlankStr
from core.utils.fake import faker
from enums.movie.locations import Location


class MovieData(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    name: NonBlankStr = Field(default_factory=lambda: " ".join(faker.words(nb=faker.random_int(1, 2))))
    image_url: NonBlankStr = Field(default_factory=faker.url)
    price: NonBlankStr = Field(default_factory=lambda: str(faker.random_int(1, 10)))
    description: NonBlankStr = Field(default_factory=lambda: faker.text(max_nb_chars=100))
    location: str = Field(default_factory=lambda: str(faker.random_element(list(Location))))
    published: datetime = Field(default_factory=datetime.now)
    genre_id: int = Field(default_factory=lambda: faker.random_int(1, 10))
