from sqlalchemy import select
from sqlalchemy.orm import Session

from models.db.genre import Genre
from models.db.movie import Movie


class MoviesDbHelper:
    def __init__(self, session: Session):
        self._session = session

    def find_movie_by_name(self, name: str) -> Movie:
        # TODO подумать о киллизиях имен и доп сортировке
        statement = select(Movie).where(Movie.name == name)
        result = self._session.execute(statement)
        return result.scalar_one()

    def get_random_genre(self) -> Genre:
        # TODO подумать о киллизиях имен и доп сортировке
        statement = select(Genre).limit(1)
        result = self._session.execute(statement)
        return result.scalar_one()
