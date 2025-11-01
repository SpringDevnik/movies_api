from pydantic import BaseModel

from core.pydantic.annotations.type import NonNegativeInt, NonBlankStr


class GenreSchema(BaseModel):
    id: NonNegativeInt
    name: NonBlankStr
