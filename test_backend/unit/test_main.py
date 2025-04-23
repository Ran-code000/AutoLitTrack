import pytest
import os
from fastapi.testclient import TestClient
from backend.app.main import app, crawler, nlp, scheduler
from backend.app.database.models import Base, Paper
from backend.app.database.config import get_db
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch
from datetime import datetime

# Shared engine for all fixtures
# Use file-based SQLite database instead of in-memory
TEST_DB_PATH = "test.db"
engine = create_engine(
    f"sqlite:///{TEST_DB_PATH}",
    connect_args={"check_same_thread": False},
    echo=True
)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

@pytest.fixture(scope="function")
def db_session():
    # Create tables
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        # Rollback and close session
        session.rollback()
        session.close()
        # Drop tables and close connections
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.rollback()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

def test_search_endpoint(client, db_session):
    mock_papers = [
        {
            "title": "Test Paper",
            "abstract": "Test abstract",
            "link": "http://example.com/test.pdf",
            "published": "2023-10-01T00:00:00",
            "keywords": ["test", "paper"]
        }
    ]
    with patch.object(crawler, "search_papers", return_value=mock_papers):
        with patch.object(nlp, "extract_keywords", return_value=["test", "paper"]):
            with patch.object(nlp, "generate_summary", return_value="Test summary"):
                response = client.get("/search?keyword=test")
                assert response.status_code == 200
                assert "results" in response.json()
                assert len(response.json()["results"]) == 1
                assert response.json()["results"][0]["title"] == "Test Paper"
                paper = db_session.query(Paper).filter_by(title="Test Paper").first()
                assert paper is not None
                assert paper.keyword == "test"

def test_papers_endpoint(client, db_session):
    # Pre-populate database
    paper = Paper(
        title="Test Paper",
        abstract="Test abstract",
        link="http://example.com/test.pdf",
        published=datetime.fromisoformat("2023-10-01T00:00:00"),
        keyword="test",
        keywords="test,paper",
        summary="Test summary"
    )
    db_session.add(paper)
    db_session.commit()
    
    response = client.get("/papers?keyword=test")
    assert response.status_code == 200
    assert "papers" in response.json()
    assert len(response.json()["papers"]) == 1
    assert response.json()["papers"][0]["title"] == "Test Paper"


def test_scheduler_status_endpoint(client):
    with patch.object(scheduler, "get_status", return_value={"running": True}):
        response = client.get("/scheduler/status")
        assert response.status_code == 200
        assert response.json() == {"running": True}

def test_search_endpoint_empty_keyword(client):
    response = client.get("/search?keyword=")
    assert response.status_code == 200
    assert response.json()["results"] == []