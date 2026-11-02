from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.subgenre import Subgenre

def get_all_by_slug(db: Session) -> dict[str, Subgenre]:
    subgenres = db.scalars(select(Subgenre)).all()
    return {s.slug: s for s in subgenres}