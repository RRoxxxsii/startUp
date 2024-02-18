import os
from dataclasses import dataclass


@dataclass(frozen=True)
class CeleryConfig:
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND")
