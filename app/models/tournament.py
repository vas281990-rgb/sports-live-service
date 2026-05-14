from sqlalchemy import Column, Integer, String

from app.core.database import Base


class Tournament(Base):
    __tablename__ = "tournaments"

    id = Column(Integer, primary_key=True)
    external_id = Column(Integer, unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    category_name = Column(String(255), nullable=True)