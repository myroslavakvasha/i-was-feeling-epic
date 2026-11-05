# backend/scripts/inspect_genres.py
import random
from collections import Counter

from sqlalchemy import select

from app.core.database import SessionLocal
from app.models import Movie  # adjust the import if needed

HORROR_ID = 27


def summarize(name: str, movies: list[Movie]) -> None:
    label_counts = Counter(len(m.subgenre_links) for m in movies)
    slug_counts = Counter(link.subgenre.slug for m in movies for link in m.subgenre_links)

    print(f"\n=== {name}: {len(movies)} labeled movies ===")
    print("Labels per movie:", {n: label_counts[n] for n in sorted(label_counts)})
    print("Top 10 labels:")
    for slug, count in slug_counts.most_common(10):
        print(f"  {count:5}  {slug}")


def main() -> None:
    with SessionLocal() as db:
        labeled = db.scalars(select(Movie).where(Movie.subgenre_links.any())).all()

        horror = [m for m in labeled if HORROR_ID in (m.tmdb_genres or [])]
        not_horror = [m for m in labeled if HORROR_ID not in (m.tmdb_genres or [])]

        summarize("Tagged Horror (27)", horror)
        summarize("NOT tagged Horror", not_horror)

        print("\n=== 15 random labeled movies NOT tagged Horror ===")
        for m in random.sample(not_horror, min(15, len(not_horror))):
            year = m.release_date.year if m.release_date else "?"
            slugs = ", ".join(link.subgenre.slug for link in m.subgenre_links)
            print(f"\n{m.title} ({year}) -> {slugs}\n  {(m.overview or '')[:250]}")


if __name__ == "__main__":
    main()