from dataclasses import dataclass
from functools import lru_cache

from src.infrastructure.database.config import PostgresConfig
from src.infrastructure.inmemory_db.config import RedisConfig
from src.infrastructure.mailing.config import SMTPMailConfig
from src.infrastructure.tasks.config import CeleryConfig


@dataclass(frozen=True)
class Settings:
    POSTGRES_DB = PostgresConfig
    CELERY = CeleryConfig
    SMTP_MAIL = SMTPMailConfig
    REDIS = RedisConfig


@lru_cache
def get_settings() -> Settings:
    return Settings()
