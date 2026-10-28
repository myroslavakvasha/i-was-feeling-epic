from datetime import date, timezone, datetime
from app.models.movie import Movie
from app.repositories import movie_repository
import httpx

def _none_if_empty(value):
    return None if value in ("", 0, None, [], {}) else value

def _parse_date(value: str | None) -> date | None:
    if not value:
        return None
    return date.fromisoformat(value)

def to_movie_fields(details: dict) -> dict:
    keywords = details.get("keywords", {}).get("keywords", [])

    return {
        "tmdb_id": details["id"],
        "title": details["title"],
        "original_title": _none_if_empty(details.get("original_title")),
        "original_language": _none_if_empty(details.get("original_language")),
        "overview": _none_if_empty(details.get("overview")),
        "tagline": _none_if_empty(details.get("tagline")),
        "release_date": _parse_date(details.get("release_date")),
        "runtime": _none_if_empty(details.get("runtime")),
        "poster_path": _none_if_empty(details.get("poster_path")),
        "budget": _none_if_empty(details.get("budget")),
        "revenue": _none_if_empty(details.get("revenue")),
        # non-nullable numbers: 0 is a real value, never None
        "vote_average": details.get("vote_average") or 0,
        "vote_count": details.get("vote_count") or 0,
        "popularity": details.get("popularity") or 0,
        # non-nullable JSON lists: empty means [], not None
        "tmdb_genres": [g["id"] for g in details.get("genres", [])],
        "production_countries": [c["iso_3166_1"] for c in details.get("production_countries", [])],
        "spoken_languages": [l["iso_639_1"] for l in details.get("spoken_languages", [])],
        "keywords": [k["name"].lower() for k in keywords],
    }

def run(db, client, max_pages=None):
    page = total_pages = 1

    while page <= total_pages:
        data = client.discover(page, with_genres="27|53|9648|18", **{"vote_count.gte": 50, "with_runtime.gte": 60})

        total_pages = min(data["total_pages"], 500)
        if max_pages is not None:
            total_pages = min(total_pages, max_pages)

        for item in data["results"]:
            tmdb_id = item["id"]

            try:
                details = client.movie_details(tmdb_id)
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    print(f"skipping {tmdb_id}: not found")
                    continue
                raise   # any other error is a real problem

            fields = to_movie_fields(details)

            movie = movie_repository.get_by_tmdb_id(db, tmdb_id)
            if movie is None:
                movie = Movie(**fields)
                movie_repository.add(db, movie)
            else:
                for k, v in fields.items():
                    setattr(movie, k, v)

            movie.synced_at = datetime.now(timezone.utc)

        db.commit()
        print(f"page {page}/{total_pages} done")
        page +=1
