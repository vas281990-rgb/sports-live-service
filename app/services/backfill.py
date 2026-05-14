from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.models.backfill_checkpoint import BackfillCheckpoint


def save_backfill_checkpoint(
    db: Session,
    source: str,
    cursor: str,
) -> None:
    # Checkpoint allows safe resume after worker restart or failure.
    stmt = (
        insert(BackfillCheckpoint)
        .values(
            source=source,
            last_cursor=cursor,
        )
        .on_conflict_do_update(
            index_elements=[BackfillCheckpoint.source],
            set_={
                "last_cursor": cursor,
            },
        )
    )
    db.execute(stmt)
    db.commit()


def get_backfill_checkpoint(
    db: Session,
    source: str,
) -> str | None:
    checkpoint = (
        db.query(BackfillCheckpoint)
        .filter(BackfillCheckpoint.source == source)
        .first()
    )
    if checkpoint is None:
        return None
    return checkpoint.last_cursor