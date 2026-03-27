from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AEGIS Backend"
    api_prefix: str = "/api/v1"
    secret_key: str = "change-me"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    database_url: str = "sqlite:///./aegis.db"
    redis_url: str = "redis://localhost:6379/0"

    openai_api_key: str = ""
    groq_api_key: str = ""
    llm_provider: str = "rule-based"
    llama_model_path: str = "models/llama-3-8b"
    mistral_model_path: str = "models/mistral-7b"

    docker_network: str = "aegis_default"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
