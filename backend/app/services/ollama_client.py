import httpx

from app.core.config import settings

class OllamaClient:
    def __init__(self) -> None:
        self._client = httpx.Client(
            base_url=settings.ollama_url,
            timeout=120
        )

    def chat(self, system: str, user: str) -> str:
        response = self._client.post(
            "/api/chat",
            json={
                "model": settings.ollama_model,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                "format": "json",
                "stream": False,
                "options": {"temperature": 0, "num_predict": 150},
            },
        )
        response.raise_for_status()
        return response.json()["message"]["content"]

    def close(self) -> None:
        self._client.close()
