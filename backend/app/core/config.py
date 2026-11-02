from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    tmdb_token: str
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = 60 * 24
    database_url: str = "sqlite:///./epic.db"
    genre_selection: str = "27|53|9648|18"
    min_vote_count: int = 50
    min_runtime: int = 60
    ollama_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2:3b"
    classifier_version: str = "llama3.2:3b-p2"

settings = Settings()