import logging
from typing import Self, Mapping

from requests import Session

from api.auth_api import AuthApi
from api.movies_api import MoviesApi


class ApiManager:
    def __init__(
        self,
        *,
        base_headers: Mapping[str, str],
        session: Session | None = None,
        logger: logging.Logger | None = None,
    ):
        """
        Инициализация ApiManager.
        :param session: HTTP-сессия, используемая всеми API-классами.
        """
        self._session = session
        self._logger = logger
        self._base_headers = base_headers

        self._auth_api: AuthApi | None = None
        self._movies_api: MoviesApi | None = None

    """
    Класс для управления API-классами с единой HTTP-сессией.
    """

    @property
    def auth(self) -> AuthApi:
        if not self._auth_api:
            self._auth_api = AuthApi(
                session=self._session,
                logger=self._logger,
                base_headers=self._base_headers,
            )
        return self._auth_api

    @property
    def movies(self) -> MoviesApi:
        if not self._movies_api:
            self._movies_api = MoviesApi(
                session=self._session,
                logger=self._logger,
                base_headers=self._base_headers,
            )
        return self._movies_api

    def reset(self) -> Self:
        self._auth_api = None
        self._movies_api = None

        if self._session:
            self._session.headers.clear()
            self._session.headers.clear()

        return self

    def close_session(self) -> None:
        if self._session:
            self._session.close()
