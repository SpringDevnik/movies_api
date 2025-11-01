from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict
from requests import Response

BaseModelChild = TypeVar("BaseModelChild", bound=BaseModel)


class HttpResponseWrapper(BaseModel, Generic[BaseModelChild]):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    response: BaseModelChild
    raw_response: Response

    def as_tuple(self) -> tuple[BaseModelChild, Response]:
        return self.response, self.raw_response
