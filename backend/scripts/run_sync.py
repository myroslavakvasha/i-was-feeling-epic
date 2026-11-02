# from app.core.database import SessionLocal
# from app.services.tmdb_client import TmdbClient
# from app.services import sync


# def main():
#     db = SessionLocal()
#     client = TmdbClient()
#     try:
#         sync.run(db, client, max_pages=1)
#     finally:
#         client.close()
#         db.close()


# if __name__ == "__main__":
#     main()


from app.core.database import SessionLocal
from app.services import sync
from app.services.tmdb_client import TmdbClient

ERAS = [
    (None, "1979-12-31"),
    ("1980-01-01", "1989-12-31"),
    ("1990-01-01", "1999-12-31"),
    ("2000-01-01", "2009-12-31"),
    ("2010-01-01", "2019-12-31"),
    ("2020-01-01", None),
]

db = SessionLocal()
client = TmdbClient()
try:
    for start, end in ERAS:
        print(f"=== Horror/Thriller/Mystery {start} to {end} ===")
        sync.run(db, client, genres="27|53|9648", min_votes=50, date_from=start, date_to=end)
    print("=== Drama, 500+ votes ===")
    sync.run(db, client, genres="18", min_votes=500)
finally:
    client.close()
    db.close()