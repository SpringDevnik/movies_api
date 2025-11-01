from abc import ABC, abstractmethod
from typing import Generic, Self, TypeVar

from pydantic import BaseModel, ConfigDict, RootModel
from pydantic.alias_generators import to_camel

T = TypeVar("T")


class RequestBaseModel(BaseModel, ABC):
    model_config = ConfigDict(
        extra="allow",
        frozen=True,
        alias_generator=to_camel,
        validate_by_alias=False,
    )


class ResponseBaseModel(BaseModel, ABC):
    model_config = ConfigDict(
        frozen=True,
        alias_generator=to_camel,
        validate_by_alias=True,
        validate_by_name=True,
        extra="forbid",
    )

    @abstractmethod
    def match(self, expected: Self) -> None:
        # TODO необходимо добавить smart match, который определяет, какие поля скипать, детектик вложенные модели (в
        # том числе в списках, словарях и тп) и вызывает их smart match рекурсивно
        # Дать возможность конкретным реализациям определять свой set игнорируемых сравнением полей
        pass


class ResponseBaseRootModel(RootModel[T], ABC, Generic[T]):
    model_config = ConfigDict(
        alias_generator=to_camel,
        validate_by_alias=False,
    )
