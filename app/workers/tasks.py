from app.core.database import SessionLocal
from app.services.normalizer import normalize_raw_snapshot
from app.workers.celery_app import celery_app


@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=30,
    retry_jitter=True,
    max_retries=5,
)
def normalize_snapshot(self, snapshot_id: int):
    # Celery retry/backoff protects us from temporary DB or worker failures.
    db = SessionLocal()
    try:
        count = normalize_raw_snapshot(db=db, snapshot_id=snapshot_id)
        return {"snapshot_id": snapshot_id, "normalized_events": count}
    finally:
        db.close()