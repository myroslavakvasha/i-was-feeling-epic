from sqlalchemy import select

from app.core.database import SessionLocal
from app.core.subgenres import SUBGENRES
from app.models import Subgenre


def main() -> None:
    with SessionLocal() as db:
        existing = {s.slug: s for s in db.scalars(select(Subgenre))}
        added = updated = 0

        for slug, name in SUBGENRES:
            row = existing.get(slug)
            if row is None:
                db.add(Subgenre(slug=slug, name=name))
                added += 1
            elif row.name != name:
                row.name = name          # keep display names in sync with the list
                updated += 1

        db.commit()
        print(f"Subgenres: {added} added, {updated} updated, {len(SUBGENRES)} total in list.")


if __name__ == "__main__":
    main()