import pytest
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from backend.app.database.models import Base, Paper
from backend.app.database.crud import save_paper, get_papers_by_keyword
from backend.app.database.config import get_db
import os

TEST_DB_PATH = "test.db"
engine = create_engine(
    f"sqlite:///{TEST_DB_PATH}",
    connect_args={"check_same_thread": False},
    echo=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()
        if os.path.exists(TEST_DB_PATH):
            try:
                os.remove(TEST_DB_PATH)
            except PermissionError:
                print(f"Warning: Could not delete {TEST_DB_PATH} due to file lock")

def test_get_db_session(db_session):
    db_gen = get_db()
    db = next(db_gen)
    assert isinstance(db, Session)
    result = db.execute(text("SELECT 1")).scalar()
    assert result == 1
    try:
        db_gen.close()
    except RuntimeError:
        pass
    assert db.close, "Session should be closed after db_gen.close()"

def test_save_paper(db_session):
    paper_data = {
        "title": "Test Paper",
        "abstract": "This is a test abstract",
        "link": "http://example.com/test.pdf",
        "published": "2023-10-01T00:00:00"
    }
    keyword = "test"
    saved_paper = save_paper(db_session, paper_data, keyword)
    assert saved_paper.title == paper_data["title"]
    assert saved_paper.abstract == paper_data["abstract"]
    assert saved_paper.link == paper_data["link"]
    assert saved_paper.published == datetime.fromisoformat(paper_data["published"])
    assert saved_paper.keyword == keyword
    paper_in_db = db_session.query(Paper).filter_by(title="Test Paper").first()
    assert paper_in_db is not None
    assert paper_in_db.keyword == keyword

def test_save_paper_missing_fields(db_session):
    paper_data = {
        "title": "Incomplete Paper",
        "abstract": "",
        "link": "http://example.com/incomplete.pdf",
        "published": "2023-10-01T00:00:00"
    }
    keyword = "incomplete"
    saved_paper = save_paper(db_session, paper_data, keyword)
    assert saved_paper.title == paper_data["title"]
    assert saved_paper.abstract == ""
    assert saved_paper.keyword == keyword

def test_get_papers_by_keyword(db_session):
    papers = [
        {
            "title": "Paper 1",
            "abstract": "Abstract 1",
            "link": "http://example.com/paper1.pdf",
            "published": "2023-10-01T00:00:00"
        },
        {
            "title": "Paper 2",
            "abstract": "Abstract 2",
            "link": "http://example.com/paper2.pdf",
            "published": "2023-10-02T00:00:00"
        }
    ]
    keyword = "machine learning"
    for paper_data in papers:
        save_paper(db_session, paper_data, keyword)
    retrieved_papers = get_papers_by_keyword(db_session, keyword, limit=10)
    assert len(retrieved_papers) == 2
    assert retrieved_papers[0].title == "Paper 1"
    assert retrieved_papers[1].title == "Paper 2"
    assert retrieved_papers[0].keyword == keyword

def test_get_papers_by_keyword_no_results(db_session):
    papers = get_papers_by_keyword(db_session, "nonexistent", limit=10)
    assert len(papers) == 0