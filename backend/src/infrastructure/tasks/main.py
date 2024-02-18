from celery import Celery

from src.infrastructure.tasks.config import CeleryConfig


app = Celery(__name__, broker_connection_retry_on_startup=True)
app.conf.broker_url = CeleryConfig.CELERY_BROKER_URL
app.conf.result_backend = CeleryConfig.CELERY_RESULT_BACKEND
