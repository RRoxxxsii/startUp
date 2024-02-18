import os
from dataclasses import dataclass


@dataclass(frozen=True)
class RedisConfig:
    HOST = os.getenv("REDIS_HOST")
