from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.event import Event

router = APIRouter()


@router.get("/monitoring/live-freshness")
def live_freshness(
    db: Session = Depends(get_db),
):
    # Freshness shows how far our normalized data is behind upstream.
    latest_update = db.query(func.max(Event.upstream_updated_at)).scalar()

    if latest_update is None:
        return {
            "status": "no_data",
            "freshness_seconds": None,
            "warning_threshold_seconds": 10,
            "critical_threshold_seconds": 30,
        }

    now = datetime.now(timezone.utc)
    freshness_seconds = (now - latest_update).total_seconds()

    if freshness_seconds > 30:
        status = "critical"
    elif freshness_seconds > 10:
        status = "warning"
    else:
        status = "ok"

    return {
        "status": status,
        "freshness_seconds": round(freshness_seconds, 3),
        "warning_threshold_seconds": 10,
        "critical_threshold_seconds": 30,
    }