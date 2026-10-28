from app.core.database import SessionLocal
from app.services.tmdb_client import TmdbClient
from app.services import sync


def main():
    db = SessionLocal()
    client = TmdbClient()
    try:
        sync.run(db, client, max_pages=1)
    finally:
        client.close()
        db.close()


if __name__ == "__main__":
    main()