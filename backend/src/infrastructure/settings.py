import os
from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PG_DSN: str = os.getenv('PG_DSN')


@lru_cache
def get_settings() -> Settings:
    return Settings()
