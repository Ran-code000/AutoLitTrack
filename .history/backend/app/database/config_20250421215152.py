# backend/app/database/config.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Database URL for SQLite
DATABASE_URL = "sqlite:///papers.db"

# Create the SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Required for SQLite to allow multi-threading
)

# Create a configured "Session" class
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    """
    Dependency function to provide a database session.
    Yields a session and ensures it is closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()