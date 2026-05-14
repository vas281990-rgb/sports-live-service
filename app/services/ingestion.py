import json
from pathlib import Path

from sqlalchemy.orm import Session

from app.models.raw_snapshot import RawSnapshot
from app.workers.tasks import normalize_snapshot


def ingest_fixture(
    db: Session,
    fixture_path: str,
    source: str = "fixture",
) -> RawSnapshot:
    # Store the original upstream-like payload before normalization.
    path = Path(fixture_path)
    with path.open("r", encoding="utf-8") as file:
        payload = json.load(file)

    snapshot = RawSnapshot(
        source=source,
        fixture_name=path.name,
        payload=payload,
    )
    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)

    # Trigger async normalization after raw snapshot is safely stored.
    normalize_snapshot.delay(snapshot.id)
    return snapshot