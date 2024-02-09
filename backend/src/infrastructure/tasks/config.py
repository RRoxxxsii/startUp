from celery import Celery

from src.infrastructure.settings import Settings


app = Celery(__name__, broker_connection_retry_on_startup=True)
app.conf.broker_url = Settings.CELERY_BROKER_URL
app.conf.result_backend = Settings.CELERY_RESULT_BACKEND
