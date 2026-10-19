import httpx
from app.core.config import settings

client = httpx.Client(
    base_url="https://api.themoviedb.org/3",
    headers={"Authorization": f"Bearer {settings.tmdb_token}"},
    timeout=15,
)

def get(path: str, **params):
    r = client.get(path, params=params)
    r.raise_for_status()
    return r.json()

# 1. Genres
genres = get("/genre/movie/list", language="en")["genres"]
genre_names = {g["id"]: g["name"] for g in genres}
print(genre_names)

# 2. Discover horror movies
page = get("/discover/movie", with_genres="27",
           sort_by="popularity.desc", page=1)
print("total:", page["total_results"], "pages:", page["total_pages"])
for m in page["results"][:5]:
    print(m["id"], m["title"], [genre_names[g] for g in m["genre_ids"]])

# 3. Details + keywords for the first one
d = get(f"/movie/{page['results'][0]['id']}", append_to_response="keywords")
print(d["title"], d["runtime"], [k["name"] for k in d["keywords"]["keywords"]])

# 4. Look up keyword ids
for k in get("/search/keyword", query="slasher")["results"][:5]:
    print(k)