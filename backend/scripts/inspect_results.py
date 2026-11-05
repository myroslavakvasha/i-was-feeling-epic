# backend/scripts/inspect_results.py
from sqlalchemy import func, select

from app.core.database import SessionLocal
from app.models import Movie, MovieSubgenre, Subgenre  # adjust if your models aren't exported from app/models/__init__.py


def print_sample(title: str, movies: list[Movie]) -> None:
    print(f"\n=== {title} ===")
    for m in movies:
        year = m.release_date.year if m.release_date else "?"
        slugs = ", ".join(link.subgenre.slug for link in m.subgenre_links) or "-"
        overview = (m.overview or "(no overview)")[:300]
        print(f"\n{m.title} ({year}) -> {slugs}\n  {overview}")


def main() -> None:
    with SessionLocal() as db:
        total = db.scalar(select(func.count()).select_from(Movie))
        classified = db.scalar(
            select(func.count()).select_from(Movie).where(Movie.classified_at.is_not(None))
        )
        with_links = db.scalar(select(func.count(func.distinct(MovieSubgenre.movie_id))))
        total_links = db.scalar(select(func.count()).select_from(MovieSubgenre))

        print(f"Total movies:            {total}")
        print(f"Classified (not NULL):   {classified}")
        print(f"With >= 1 subgenre:      {with_links}")
        print(f"With 0 subgenres:        {classified - with_links}")
        print(f"Total links:             {total_links}")

        print("\n=== Movies per subgenre ===")
        rows = db.execute(
            select(Subgenre.slug, func.count(MovieSubgenre.movie_id))
            .outerjoin(MovieSubgenre, MovieSubgenre.subgenre_id == Subgenre.id)
            .group_by(Subgenre.slug)
            .order_by(func.count(MovieSubgenre.movie_id).desc())
        ).all()
        for slug, count in rows:
            print(f"{count:6}  {slug}")

        labeled = db.scalars(
            select(Movie).where(Movie.subgenre_links.any()).order_by(func.random()).limit(20)
        ).all()
        print_sample("20 random LABELED movies", labeled)

        unlabeled = db.scalars(
            select(Movie)
            .where(Movie.classified_at.is_not(None), ~Movie.subgenre_links.any())
            .order_by(func.random())
            .limit(10)
        ).all()
        print_sample("10 random movies with 0 labels", unlabeled)


if __name__ == "__main__":
    main()