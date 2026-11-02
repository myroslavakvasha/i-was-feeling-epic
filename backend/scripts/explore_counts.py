from app.services.tmdb_client import TmdbClient

client = TmdbClient()

def count(label, genres, min_votes, date_from=None, date_to=None):
    filters = {"vote_count.gte": min_votes}
    if date_from:
        filters["primary_release_date.gte"] = date_from
    if date_to:
        filters["primary_release_date.lte"] = date_to
    data = client.discover(1, with_genres=genres, **filters)
    print(f"{label}: {data['total_results']} results, {data['total_pages']} pages")

eras = [
    ("up to 1979", None, "1979-12-31"),
    ("1980s", "1980-01-01", "1989-12-31"),
    ("1990s", "1990-01-01", "1999-12-31"),
    ("2000s", "2000-01-01", "2009-12-31"),
    ("2010s", "2010-01-01", "2019-12-31"),
    ("2020+", "2020-01-01", None),
]

for label, start, end in eras:
    count(label, "27|53|9648", 50, start, end)

count("Drama, 500 votes", "18", 500)
client.close()