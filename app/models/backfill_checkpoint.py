from sqlalchemy import Column, DateTime, Integer, String, func

from app.core.database import Base


class BackfillCheckpoint(Base):
    __tablename__ = "backfill_checkpoints"

    id = Column(Integer, primary_key=True)
    source = Column(String(64), unique=True, nullable=False)
    # Stores latest processed cursor/timestamp for safe backfill resume.
    last_cursor = Column(String(255), nullable=True)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )