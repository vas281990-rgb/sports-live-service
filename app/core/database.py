from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Main PostgreSQL engine.
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
)

# Session factory for API and workers.
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

# Base class for all SQLAlchemy models.
Base = declarative_base()


def get_db():
    # FastAPI dependency for safe DB session lifecycle.
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()