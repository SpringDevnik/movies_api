from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from core.db.sqlalchemy.base_db_client import BaseDbClient


class PgClient(BaseDbClient[Session]):

    def __init__(
        self,
        *,
        username: str,
        password: str,
        host: str,
        port: str,
        database_name: str,
    ):
        super().__init__(
            username=username,
            password=password,
            host=host,
            port=port,
            database_name=database_name,
        )
        url = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database_name}"
        self._engine = create_engine(url)
        self._Session = sessionmaker(self._engine, autoflush=False)

    def get_new_db_session(self) -> Session:
        return self._Session()
