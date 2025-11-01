import logging
from typing import Any, override, TypeVar, Type, Mapping

import allure
from pydantic import BaseModel
from requests import Session, Request

from core.http.base_http_client import BaseHttpClient
from core.http.requests.logging import allure_log_request, local_log_request, local_log_response
from core.pydantic.models.response_wrapper import HttpResponseWrapper
from _settings import settings

T = TypeVar("T", bound=BaseModel)


class HttpClient(BaseHttpClient):
    """
    Кастомный HTTP-клиент для стандартизации и упрощения отправки
    HTTP-запросов.
    """

    def __init__(
        self,
        base_url: str,
        base_headers: Mapping[str, str] = settings.api.BASE_HEADERS,
        session: Session | None = None,
        logger: logging.Logger | None = None,
    ) -> None:
        """
        Инициализация кастомного HTTP-клиента.
        :param session: Объект http.Session.
        :param base_url: Базовый URL API.
        :param base_headers: Словарь базовых заголовков.
        """
        base_headers = dict(base_headers)
        super().__init__(
            base_url=base_url,
            base_headers=base_headers,
        )
        self.session = session or Session()
        self.session.headers.update(base_headers)
        self.logger = logger or logging.getLogger(__name__)

    @allure.step("Отправка запроса на сервер")
    @override
    def _send_request(
        self,
        *,
        method: str,
        endpoint: str,
        response_model: Type[T],
        params: dict[str, Any] | None = None,
        json: Any | None = None,
    ) -> HttpResponseWrapper[T]:
        """
        Универсальный метод для отправки запросов.
        :param method: HTTP метод (GET, POST, PUT, DELETE и т.д.).
        :param endpoint: Эндпоинт (например, "/login").
        :param params: Параметры запроса.
        :param json: Тело запроса (JSON-данные).
        :return: Объект ответа http.Response.
        """
        url = f"{self.base_url}{endpoint}"

        request = Request(
            method=method,
            url=url,
            params=params,
            json=json,
        )
        prepared_request = self.session.prepare_request(request)

        local_log_request(self.logger, prepared_request)
        allure_log_request(prepared_request)

        raw_response = self.session.send(request=prepared_request)

        local_log_response(self.logger, raw_response)

        model = response_model.model_validate(
            raw_response.json(),
            by_alias=True,
        )
        return HttpResponseWrapper(
            response=model,
            raw_response=raw_response,
        )

    def post(
        self,
        *,
        endpoint: str,
        response_model: Type[T],
        json: dict[str, Any] | None = None,
    ) -> HttpResponseWrapper[T]:
        return self._send_request(
            method="POST",
            endpoint=endpoint,
            json=json,
            response_model=response_model,
        )

    def get(
        self,
        *,
        endpoint: str,
        response_model: Type[T],
        params: dict[str, Any] | None = None,
    ) -> HttpResponseWrapper[T]:
        return self._send_request(
            method="GET",
            endpoint=endpoint,
            params=params,
            response_model=response_model,
        )

    def delete(
        self,
        *,
        endpoint: str,
        response_model: Type[T],
        params: dict[str, Any] | None = None,
    ) -> HttpResponseWrapper[T]:
        return self._send_request(
            method="DELETE",
            endpoint=endpoint,
            params=params,
            response_model=response_model,
        )

    def patch(
        self,
        *,
        endpoint: str,
        response_model: Type[T],
        json: dict[str, Any] | None = None,
    ) -> HttpResponseWrapper[T]:
        return self._send_request(
            method="PATCH",
            endpoint=endpoint,
            json=json,
            response_model=response_model,
        )

    def _update_session_headers(self, **kwargs: object) -> None:
        """
        Обновление заголовков сессии.
        :param kwargs: Дополнительные заголовки.
        """
        self.headers.update(kwargs)
        self.session.headers.update(self.headers)
