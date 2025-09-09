import pytest
from requests import Response
from urllib3.exceptions import HTTPError

from asserters.movies_asserters import assert_genre_exist


class TestCreateMovie:

    def test_create_nonexistent_movie(
            self,
            super_admin_token,
            random_movie_data,
            api_manager,
    ):
        api_manager.movies_api._update_session_headers(
            **{"Authorization": f"Bearer {super_admin_token}"},
        )

        response_data = api_manager.movies_api.create_movie(
            movie_data=random_movie_data,
        ).json()

        assert response_data["id"] > 0, "id не может быть отрицательным"
        assert response_data["name"] == random_movie_data["name"], (
            "name должно быть такое же, как в реквесте"
        )
        assert response_data["price"] == random_movie_data["price"], (
            "цена не совпадает"
        )
        assert response_data["description"] == random_movie_data[
            "description"], (
            "описание фильма не совпадает"
        )
        assert response_data["imageUrl"] == random_movie_data["imageUrl"], (
            "imageUrl фильма не совпадает"
        )
        assert response_data["location"] == random_movie_data["location"], (
            "страна фильма не совпадает"
        )
        assert response_data["published"] == random_movie_data["published"], (
            "статус публикации фильма не совпадает"
        )
        assert len(response_data["genre"]) == 1, (
            "жанров фильма больше ожидаемого"
        )
        assert_genre_exist(
            genreId=response_data["genreId"],
            genreName=response_data["genre"]["name"],
        )
        # ассертер на дату не добавлял, так как нет инфы о тайм-зоне сервера
        assert response_data["rating"] == 0, (
            "рейтинг не равен значению по умолчанию"
        )

    @pytest.mark.skip(reason="Отсутствует валидация имени")
    def test_create_movie_with_negative_price(
            self,
            super_admin_token,
            random_movie_data,
            api_manager,
    ):
        random_movie_data["price"] = -1

        with pytest.raises(HTTPError):
            response: Response = api_manager.movies_api.create_movie(
                movie_data=random_movie_data,
            ).json()

        assert response.status_code == 400
        assert response.json()["message"] == ("price cannot be "
                                              "lover then 0"), (
            "Сообщение об ошибке не совпадает с ожидаемым"
        )
        assert response.json()["statusCode"] == 400, "неверный статус код"
