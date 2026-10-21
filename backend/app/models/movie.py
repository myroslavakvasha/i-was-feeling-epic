from sqlalchemy import String, Text, BigInteger, JSON
from datetime import date, datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.movie_subgenre import MovieSubgenre

class Movie(Base):
    __tablename__ = "movie"

    id: Mapped[int] = mapped_column(primary_key=True)
    tmdb_id: Mapped[int] = mapped_column(unique=True)
    title: Mapped[str] = mapped_column(String(300))
    original_title: Mapped[str | None] = mapped_column(String(300))
    original_language: Mapped[str | None] = mapped_column(String(8))
    overview: Mapped[str | None] = mapped_column(Text)
    tagline: Mapped[str | None] = mapped_column(Text)
    release_date: Mapped[date | None]
    runtime: Mapped[int | None]
    poster_path: Mapped[str | None] = mapped_column(String)
    budget: Mapped[int | None] = mapped_column(BigInteger)
    revenue: Mapped[int | None] = mapped_column(BigInteger)
    vote_average: Mapped[float] = mapped_column(default=0)
    vote_count: Mapped[int] = mapped_column(default=0)
    popularity: Mapped[float] = mapped_column(default=0)
    tmdb_genres: Mapped[list[int]] = mapped_column(JSON, default=list)
    production_countries: Mapped[list[str]] = mapped_column(JSON, default=list)
    spoken_languages: Mapped[list[str]] = mapped_column(JSON, default=list)
    keywords: Mapped[list[str]] = mapped_column(JSON, default=list)
    embedding: Mapped[list[float] | None] = mapped_column(JSON)
    classified_at: Mapped[datetime | None]
    synced_at: Mapped[datetime | None]

    subgenre_links: Mapped[list["MovieSubgenre"]] = relationship(back_populates="movie", cascade="all, delete-orphan")
