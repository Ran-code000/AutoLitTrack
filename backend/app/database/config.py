# backend/app/database/config.py
import os
from .models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Use test database for tests, production database otherwise
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///papers.db"
)
if "pytest" in os.environ.get("PYTEST_VERSION", ""):
    DATABASE_URL = "sqlite:///test.db"  # In-memory for tests

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=True
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

def init_db():
    """Initialize database tables (called at app startup)."""
    Base.metadata.create_all(engine)