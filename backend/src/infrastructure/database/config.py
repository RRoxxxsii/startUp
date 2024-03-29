import os
from dataclasses import dataclass


@dataclass(frozen=True)
class PostgresConfig:
    PG_DSN: str = os.getenv("PG_DSN")
