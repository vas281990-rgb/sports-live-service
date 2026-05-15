from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.ingestion import ingest_fixture

router = APIRouter()


@router.post("/sport/football/ingest-fixture")
def ingest_live_events_fixture(
    db: Session = Depends(get_db),
):
    snapshot = ingest_fixture(
        db=db,
        fixture_path="fixture/live_events.json",
    )
    return {
        "status": "accepted",
        "snapshot_id": snapshot.id,
        "message": "Raw snapshot stored and normalization task scheduled.",
    }