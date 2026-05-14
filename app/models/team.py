from sqlalchemy import Column, Integer, String

from app.core.database import Base


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True)
    external_id = Column(Integer, unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)