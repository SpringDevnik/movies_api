from datetime import datetime

from sqlalchemy import Boolean, DateTime, Double, Enum, Integer, String
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from core.db.sqlalchemy.models.base import Base
from enums.movie.locations import Location


class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    price: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(String)
    image_url: Mapped[str] = mapped_column(String)
    location: Mapped[Location] = mapped_column(Enum(Location))
    published: Mapped[bool] = mapped_column(Boolean)
    rating: Mapped[float] = mapped_column(Double)
    genre_id: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime)
