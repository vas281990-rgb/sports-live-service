from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "sports_live_worker",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["app.workers.tasks"],
)

celery_app.conf.broker_connection_retry_on_startup = True