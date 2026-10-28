from app.services.tmdb_client import TmdbClient
from app.services.sync import to_movie_fields

client = TmdbClient()
try:
    details = client.movie_details(694)   # The Shining
    print(to_movie_fields(details))
finally:
    client.close()