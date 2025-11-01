import logging
from typing import Optional, Mapping

import allure
from requests import Session

from core.http.requests.http_client import HttpClient
from core.pydantic.models.response_wrapper import HttpResponseWrapper
from enums.movie.endpoints import Endpoint
from models.api.movies.create_movie import CreateMovieRequest, CreateMovieResponse
from models.api.movies.delete_movie import DeleteMovieResponse
from models.api.movies.get_genres_list import GetGenresListResponse
from models.api.movies.get_movies import GetMoviesParams, GetMoviesResponse
from models.api.movies.patch_movie import PatchMovieRequest, PatchMovieResponse
from settings import settings


class MoviesApi(HttpClient):

    def __init__(
        self,
        base_headers: Mapping[str, str] = settings.api.BASE_HEADERS,
        base_url: str = settings.api.MOVIES_API_BASE_URL,
        session: Optional[Session] = None,
        logger: logging.Logger | None = None,
    ):
        super().__init__(
            base_headers=base_headers,
            base_url=base_url,
            session=session,
            logger=logger,
        )

    @allure.step("Создать фильм")
    def create_movie(
        self,
        request: CreateMovieRequest,
    ) -> HttpResponseWrapper[CreateMovieResponse]:
        return self.post(
            endpoint=str(Endpoint.MOVIES),
            json=request.model_dump(by_alias=True),
            response_model=CreateMovieResponse,
        )

    @allure.step("Удалить фильм")
    def delete_movie(
        self,
        movie_id: int,
    ) -> HttpResponseWrapper[DeleteMovieResponse]:
        return self.delete(
            endpoint=f"{Endpoint.MOVIES}/{movie_id}",
            response_model=DeleteMovieResponse,
        )

    @allure.step("Редактировать фильм")
    def patch_movie(
        self,
        *,
        movie_id: int,
        request: PatchMovieRequest,
    ) -> HttpResponseWrapper[PatchMovieResponse]:
        return self.patch(
            endpoint=f"{Endpoint.MOVIES}/{movie_id}",
            response_model=PatchMovieResponse,
            json=request.model_dump(by_alias=True),
        )

    @allure.step("Получить список фильмов")
    def get_movies(
        self,
        params: GetMoviesParams,
    ) -> HttpResponseWrapper[GetMoviesResponse]:
        return self.get(
            endpoint=str(Endpoint.MOVIES),
            params=params.model_dump(by_alias=True),
            response_model=GetMoviesResponse,
        )

    @allure.step("Получить список жанров фильмов")
    def get_genres_list(self) -> HttpResponseWrapper[GetGenresListResponse]:
        return self.get(
            endpoint=str(Endpoint.GENRES),
            response_model=GetGenresListResponse,
        )
