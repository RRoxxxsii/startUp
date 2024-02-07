import os
from dataclasses import dataclass
from functools import lru_cache


@dataclass
class Settings:
    PG_DSN: str = os.getenv("PG_DSN")


@lru_cache
def get_settings() -> Settings:
    return Settings()
