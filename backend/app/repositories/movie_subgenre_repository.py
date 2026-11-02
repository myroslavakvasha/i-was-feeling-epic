from sqlalchemy.orm import Session
from app.models.movie_subgenre import MovieSubgenre

def add(db: Session, link: MovieSubgenre) -> MovieSubgenre:
    db.add(link)
    return link