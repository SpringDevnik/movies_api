from typing import Annotated

from pydantic import Field

from core.pydantic.annotations._validator import non_blank_str_validator

type NonBlankStr = Annotated[str, non_blank_str_validator]
type PositiveInt = Annotated[int, Field(gt=0)]
type NonNegativeInt = Annotated[int, Field(ge=0)]
