import datetime
from typing import cast

import allure
import pytest

from core.asserters.common_asserters import equal, is_status_code
from fixtures.models.movies.user_context import UserContext
from helpers.db.movies_db_helper import MoviesDbHelper
from models.api.movies.common.genre import Genre
from models.api.movies.create_movie import CreateMovieRequest, CreateMovieResponse


@allure.epic("movie")
@allure.feature("Создание фильма")
class TestCreateMovie:

    @allure.story("Успешное создание фильма")
    @allure.description("Создание нового фильма")
    @allure.label("owner", "Andrey")
    def test_create_movie_when_nonexist(
        self,
        f_super_admin_ctx: UserContext,
        s_movie_db_helper: MoviesDbHelper,
    ) -> None:
        # TODO нужно изначально получать существующий жанр вместо хардкода
        request = CreateMovieRequest(genre_id=1)
        expected_response = CreateMovieResponse(
            id=1,  # UNPREDICTABLE
            name=request.name,
            price=request.price,
            description=request.description,
            image_url=request.image_url,
            location=request.location,
            published=request.published,
            genre_id=request.genre_id,
            genre=Genre(name="UNPREDICTABLE"),
            created_at=datetime.datetime.now(),  # UNPREDICTABLE
            rating=0,
        )
        response_wrapper = f_super_admin_ctx.api_manager.movies.create_movie(
            request=request,
        )
        response_model, response = response_wrapper.as_tuple()
        is_status_code(201, response)
        response_model.match(expected_response)

        movie = s_movie_db_helper.find_movie_by_name(cast(str, request.name))
        equal(movie.price, request.price, "price")
        equal(movie.description, request.description, "description")
        equal(movie.image_url, request.image_url, "image_url")
        # TODO остальные поля сравнивать не стал (лень)
        # TODO быть может, стоит написать кастомный конвертер моделей

    @allure.story("Неуспешное создание фильма")
    @allure.description("Создание нового фильма с отрицательной ценой")
    @allure.label("owner", "Andrey")
    @pytest.mark.skip(reason="Отсутствует валидация имени")
    def test_create_movie_when_price_negative(
        self,
        super_admin_ctx: UserContext,
    ) -> None:
        request = CreateMovieRequest(price=-1)
        raw_response = super_admin_ctx.api_manager.movies.create_movie(request).raw_response

        is_status_code(400, raw_response)
        equal(
            "price cannot be lover then 0",
            raw_response.json()["message"],
            "message",
        )
