from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Index, Integer, String, func

from app.core.database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    external_id = Column(Integer, unique=True, nullable=False, index=True)
    tournament_id = Column(Integer, ForeignKey("tournaments.id"), nullable=False)
    home_team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    away_team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    status = Column(String(64), nullable=False)
    status_description = Column(String(255), nullable=True)
    # Requirement: filter only isEditor=true.
    is_editor = Column(Boolean, nullable=False, default=False, index=True)
    start_time = Column(DateTime(timezone=True), nullable=True)
    # Used for live freshness monitoring.
    upstream_updated_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


Index("ix_events_hot_path", Event.is_editor, Event.status, Event.updated_at)