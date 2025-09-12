from typing import Dict, Any

import requests
from requests import Session, Response

from api.dto.genre import Genre
from constants import MOVIES_API_BASE_URL, BASE_HEADERS
from core.http_client import HttpClient
from enums.movie.endpoints import Endpoint


class MoviesApi(HttpClient):
    def __init__(
            self,
            session: Session = None,
            base_url: str = MOVIES_API_BASE_URL,
            base_headers: Dict[str, str] = BASE_HEADERS.copy(),
    ):
        session_ = requests.Session() if session is None else session
        super().__init__(session_, base_url, base_headers)

    def create_movie(
            self,
            movie_data: Dict[str, Any],
            expected_status=201,
    ) -> Response:
        return self.send_request(
            method="POST",
            endpoint=Endpoint.POST_MOVIES.value,
            data=movie_data,
            expected_status=expected_status,
        )

    def get_genres_list_response(
            self,
            expected_status=200,
    ) -> Response:
        return self.send_request(
            method="POST",
            endpoint=Endpoint.GET_GENRES.value,
            expected_status=expected_status,
        )

    def get_genres_list(
            self,
            expected_status=200,
    ) -> list[Genre]:
        response_data = self.send_request(
            method="GET",
            endpoint=Endpoint.GET_GENRES.value,
            expected_status=expected_status,
        ).json()
        return [
            Genre(id=genre_info["id"], name=genre_info["name"])
            for genre_info
            in response_data
        ]
