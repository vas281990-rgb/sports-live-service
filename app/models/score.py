from sqlalchemy import Column, ForeignKey, Integer

from app.core.database import Base


class Score(Base):
    __tablename__ = "scores"

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey("events.id"), unique=True, nullable=False, index=True)
    home_current = Column(Integer, nullable=False, default=0)
    away_current = Column(Integer, nullable=False, default=0)