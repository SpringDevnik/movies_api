from abc import ABC, abstractmethod
from typing import Any, TypeVar, Mapping, Type

from pydantic import BaseModel

from core.pydantic.models.response_wrapper import HttpResponseWrapper

PydanticModel = TypeVar("PydanticModel", bound=BaseModel)


class BaseHttpClient(ABC):

    @abstractmethod
    def __init__(
        self,
        base_url: str,
        base_headers: Mapping[str, Any],
    ):
        """
        Инициализация клиента.
        :param base_url: Базовый URL API.
        :param base_headers: Словарь базовых заголовков.
        """
        self.base_url = base_url
        self.headers = dict(base_headers)

    @abstractmethod
    def _send_request(
        self,
        *,
        method: str,
        endpoint: str,
        response_model: Type[PydanticModel],
        params: dict[str, Any] | None = None,
        json: Any | None = None,
    ) -> HttpResponseWrapper[PydanticModel]:
        pass
