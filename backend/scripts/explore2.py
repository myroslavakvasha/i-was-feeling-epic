from collections import Counter
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

# A. How many horror movies survive a vote filter?
for votes in (0, 10, 50, 200):
    r = get("/discover/movie", with_genres="27", **{"vote_count.gte": votes})
    print(f"horror, vote_count >= {votes}: {r['total_results']}")

# B. Non-horror movies that carry horror keywords (the "unsettling thriller/drama" cases)
slasher_ids = "12339|325981|325992|319666"
r = get("/discover/movie", with_keywords=slasher_ids, without_genres="27")
print("slasher keywords but NOT genre horror:", r["total_results"])
for m in r["results"][:8]:
    print("  ", m["title"])

# C. Most common keywords across ~200 popular horror movies
counter = Counter()
for page in range(1, 11):
    results = get("/discover/movie", with_genres="27", sort_by="popularity.desc",
                  page=page, **{"vote_count.gte": 200})["results"]
    for m in results:
        d = get(f"/movie/{m['id']}", append_to_response="keywords")
        for k in d["keywords"]["keywords"]:
            counter[k["name"]] += 1
    print("page", page, "done")

for name, count in counter.most_common(80):
    print(f"{count:4d}  {name}")