# backend/app/database/config.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

url = "sqlite:///papers.db"

engine = create_engine(
    url,
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