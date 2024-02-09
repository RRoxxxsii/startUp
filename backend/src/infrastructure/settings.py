import os
from dataclasses import dataclass
from functools import lru_cache


@dataclass
class Settings:
    PG_DSN: str = os.getenv("PG_DSN")

    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND")


@lru_cache
def get_settings() -> Settings:
    return Settings()
