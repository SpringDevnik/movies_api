from requests import Session

from api.auth_api import AuthApi
from api.movie_api import MoviesApi


class ApiManager:
    """
    Класс для управления API-классами с единой HTTP-сессией.
    """

    def __init__(self, session: Session):
        """
        Инициализация ApiManager.
        :param session: HTTP-сессия, используемая всеми API-классами.
        """
        self.session = session
        self.auth_api = AuthApi(session)
        self.movies_api = MoviesApi(session)
