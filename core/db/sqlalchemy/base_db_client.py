from abc import ABC, abstractmethod
from typing import Generic

from typing_extensions import TypeVar

SessionType = TypeVar("SessionType")


class BaseDbClient(ABC, Generic[SessionType]):
    def __init__(
        self,
        *,
        username: str,
        password: str,
        host: str,
        port: str,
        database_name: str,
    ):
        self._username = username
        self._password = password
        self._host = host
        self._port = port
        self._database_name = database_name

    @abstractmethod
    def get_new_db_session(self) -> SessionType:
        pass
