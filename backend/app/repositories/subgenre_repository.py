from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.subgenre import Subgenre
from collections.abc import Sequence

def get_slug_to_subgenre_map(db: Session) -> dict[str, Subgenre]:
    subgenres = db.scalars(select(Subgenre)).all()
    return {s.slug: s for s in subgenres}

def get_all(db: Session) -> Sequence[Subgenre]: # .all() returns sequence
    return db.scalars(select(Subgenre).order_by(Subgenre.name)).all()