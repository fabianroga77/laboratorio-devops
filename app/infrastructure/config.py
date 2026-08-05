import os
from functools import lru_cache


class Settings:
    app_name: str = "Core Banking Lite"
    app_env: str = os.getenv("APP_ENV", "development")
    app_version: str = os.getenv("APP_VERSION", "3.0.0")


@lru_cache
def get_settings() -> Settings:
    return Settings()
