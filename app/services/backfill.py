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
            # Match record by the 'source' unique identifier
            index_elements=[BackfillCheckpoint.source],
            # Update only the cursor value to the latest position
            set_={
                "last_cursor": cursor,
            },
        )
    )
    db.execute(stmt) # Execute the query
    db.commit() # Commit changes to the database


def get_backfill_checkpoint(
    db: Session,
    source: str,
) -> str | None:
    # Retrieve the last saved cursor position for a specific data source
    checkpoint = (
        db.query(BackfillCheckpoint)
        .filter(BackfillCheckpoint.source == source)
        .first()
    )
    # Return None if no checkpoint exists for this source
    if checkpoint is None:
        return None
    return checkpoint.last_cursor