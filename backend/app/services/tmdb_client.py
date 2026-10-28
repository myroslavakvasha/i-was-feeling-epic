import time
import httpx

from app.core.config import settings


class TmdbClient:
    def __init__(self) -> None:
        self._client = httpx.Client(
            base_url="https://api.themoviedb.org/3",
            headers={"Authorization": f"Bearer {settings.tmdb_token}"},
            timeout=15.0,
        )

    def _get(self, path: str, **params) -> dict:
        for attempt in range(5):
            resp = self._client.get(path, params=params)
            if resp.status_code == 429:                       # rate limited
                time.sleep(float(resp.headers.get("Retry-After", 2)))
                continue
            if resp.status_code >= 500:                       # TMDB hiccup
                time.sleep(2 ** attempt)
                continue
            resp.raise_for_status()
            return resp.json()
        raise RuntimeError(f"TMDB request failed after retries: {path}")

    def discover(self, page: int, **filters) -> dict:
        return self._get("/discover/movie", page=page, **filters)

    def movie_details(self, tmdb_id: int) -> dict:
        return self._get(f"/movie/{tmdb_id}", append_to_response="keywords")

    def close(self) -> None:
        self._client.close()