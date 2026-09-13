from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "BookShelf API"
    database_url: str
    openlibrary_base_url: str = "https://openlibrary.org"
    request_timeout_settings: float = 0.5

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings() -> Settings:
    return Settings()
