import math
from typing import cast

import allure
import pytest
from _pytest.mark import ParameterSet

from api.movies_api import MoviesApi
from core.asserters.common_asserters import compare_dates, equal, is_status_code_200
from enums.movie.locations import Location
from enums.movie.sort_order import SortOrder
from models.api.movies.get_movies import GetMoviesParams, _Movie


@allure.epic("movie")
@allure.feature("Получение фильма")
class TestGetMovies:

    @staticmethod
    def _generate_params_positive() -> list[ParameterSet]:
        params = (
            GetMoviesParams(
                page_size=1,
                page=1,
                min_price=1,
                max_price=99_999,
                locations=[Location.SPB],
                published=True,
                genre_id=1,
                create_at=SortOrder.ASC,
            ),
            GetMoviesParams(
                page_size=1,
                page=1,
                min_price=1,
                max_price=99_999,
                locations=[Location.SPB],
                published=True,
                genre_id=1,
                create_at=SortOrder.DESC,
            ),
        )
        return [pytest.param(param, id=str(param)) for param in params]

    @allure.story("Успешное получение фильма")
    @allure.description("Получение существующего фильма")
    @allure.label("owner", "Andrey")
    @pytest.mark.parametrize(
        "params",
        _generate_params_positive(),
    )
    def test_get_movies(
        self,
        params: GetMoviesParams,
        s_movies_api: MoviesApi,
    ) -> None:
        model, response = s_movies_api.get_movies(params).as_tuple()

        is_status_code_200(response)
        equal(model.page_size, params.page_size, "page_size")
        equal(model.page, params.page, "page")
        equal(
            model.page_count,
            math.ceil(model.count / cast(int, params.page_size)),
            "page_count",
        )

        if model.movies and params.create_at:
            TestGetMovies._check_movies_sorted(model.movies, params.create_at)
        else:
            equal(model.count, 0, "count")

    @staticmethod
    def _check_movies_sorted(movies: list[_Movie], create_at: str) -> None:
        for current_movie, next_movie in zip(movies, movies[1:]):
            current_elem_created_at = current_movie.created_at
            next_elem_created_at = next_movie.created_at
            if create_at == str(SortOrder.ASC):
                compare_dates(
                    actual=current_elem_created_at,
                    expected=next_elem_created_at,
                    comparison="<=",
                )
            elif create_at == str(SortOrder.DESC):
                compare_dates(
                    actual=current_elem_created_at,
                    expected=next_elem_created_at,
                    comparison=">=",
                )
