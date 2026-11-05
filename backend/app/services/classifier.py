# classifying movies into custom subgenres using ollama_client, run by scripts/run_classify.py

import json
from datetime import datetime, timezone

import httpx
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.subgenres import SUBGENRE_SLUGS, subgenres_for_prompt
from app.models.movie_subgenre import MovieSubgenre
from app.repositories import movie_repository, movie_subgenre_repository, subgenre_repository
from app.services.ollama_client import OllamaClient

MAX_LABELS = 3
MAX_CONSECUTIVE_FAILURES = 5
MODIFIER_SLUGS = {"slow-burn", "elevated-horror"}

SYSTEM_PROMPT = f"""You classify movies into horror subgenres.
Choose 0 to {MAX_LABELS} slugs from the list below that clearly describe the movie.
If none fit, return an empty list. Never invent slugs.
The movie data may include Keywords. They are hints only; the overview matters more.
Never copy keywords into the answer, only slugs from the list.
Answer only with JSON: {{"subgenres": ["slug", ...]}}

Subgenres:
{subgenres_for_prompt()}
"""

def build_user_message(movie, use_keywords: bool = True) -> str:
    text = f"Title: {movie.title}\nOverview: {movie.overview}"
    if use_keywords and movie.keywords:
        text += f"\nKeywords: {', '.join(movie.keywords)}"
    return text


def ask_ollama(client: OllamaClient, movie, use_keywords: bool = True) -> list[str]:
    try:
        raw = client.chat(SYSTEM_PROMPT, build_user_message(movie, use_keywords))
        data = json.loads(raw)
    except json.JSONDecodeError:
        if not use_keywords:
            raise   # already tried without keywords, let the loop skip it
        return ask_ollama(client, movie, use_keywords=False)

    slugs = data.get("subgenres", [])
    valid = [s for s in slugs if s in SUBGENRE_SLUGS]
    valid = list(dict.fromkeys(valid))[:MAX_LABELS]
    if all(s in MODIFIER_SLUGS for s in valid):
        return []
    return valid

def run(db: Session, client: OllamaClient, batch_size: int = 50) -> None:
    subgenres = subgenre_repository.get_slug_to_subgenre_map(db)
    failed_ids: set[int] = set()
    consecutive_failures = 0
    done = 0

    while True:
        movies = movie_repository.list_unclassified(db, batch_size, failed_ids)
        if not movies:
            break

        for movie in movies:
            try:
                slugs = ask_ollama(client, movie)
            except (json.JSONDecodeError, KeyError, TypeError, httpx.HTTPError) as e:
                print(f"FAILED {movie.title}: {e!r}")
                failed_ids.add(movie.id)
                consecutive_failures += 1
                if consecutive_failures >= MAX_CONSECUTIVE_FAILURES:
                    db.commit()
                    print("Too many failures in a row (is Ollama running?). Stopping.")
                    return
                continue

            consecutive_failures = 0
            for slug in slugs:
                link = MovieSubgenre(
                    movie_id=movie.id,
                    subgenre_id=subgenres[slug].id,
                    classifier_version=settings.classifier_version,
                )
                movie_subgenre_repository.add(db, link)

            movie.classified_at = datetime.now(timezone.utc)
            done += 1
            print(f"[{done}] {movie.title}: {slugs}")

        db.commit()