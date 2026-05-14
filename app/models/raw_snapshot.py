from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB

from app.core.database import Base


class RawSnapshot(Base):
    __tablename__ = "raw_snapshots"

    id = Column(Integer, primary_key=True)
    source = Column(String(64), nullable=False, index=True)
    fixture_name = Column(String(255), nullable=True)
    # Original upstream payload for replay, debugging and fallback.
    payload = Column(JSONB, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)