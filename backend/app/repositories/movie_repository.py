from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.movie import Movie

def get_by_tmdb_id(db: Session, tmdb_id: int) -> Movie | None:
    return db.scalar(select(Movie).where(Movie.tmdb_id == tmdb_id))

def add(db: Session, movie: Movie) -> Movie:
    db.add(movie)
    return movie

def list_unclassified(db: Session, limit: int, exclude_ids: set[int]) -> list[Movie]:
    query = (
        select(Movie)
        .where(Movie.classified_at.is_(None))
        .where(Movie.id.not_in(exclude_ids))
        .order_by(Movie.id)
        .limit(limit)
    )
    return list(db.scalars(query).all())