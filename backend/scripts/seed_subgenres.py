from sqlalchemy import select

from app.core.database import SessionLocal
from app.core.subgenres import SUBGENRES, SUBGENRE_SLUGS
from app.models.subgenre import Subgenre


def main():
    db = SessionLocal()
    try:
        existing = {s.slug: s for s in db.scalars(select(Subgenre))}
        added = updated = removed = 0

        for slug, name, _description in SUBGENRES:
            row = existing.get(slug)
            if row is None:
                db.add(Subgenre(slug=slug, name=name))
                added += 1
            elif row.name != name:
                row.name = name
                updated += 1

        for slug, row in existing.items():
            if slug not in SUBGENRE_SLUGS:
                db.delete(row)
                removed += 1

        db.commit()
        print(f"{added} added, {updated} updated, {removed} removed")
    finally:
        db.close()


if __name__ == "__main__":
    main()