from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "sports_live_worker",
    broker=settings.redis_url,
    backend=settings.redis_url,
)
