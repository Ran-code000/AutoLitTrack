import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.database.models import Base, Paper
from backend.app.database.crud import save_paper, get_papers_by_keyword

# Fixture to create a temporary in-memory database
@pytest.fixture
def db_session():
    # Use in-memory SQLite database for testing
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close() 

def test_save_paper(db_session):
    # Test data
    paper_data = {
        "title": "Test Paper",
        "abstract": "This is a test abstract",
        "link": "http://example.com/test.pdf",
        "published": "2023-10-01T00:00:00"
    }
    keyword = "test"

    # Save paper
    saved_paper = save_paper(db_session, paper_data, keyword)

    # Verify saved paper
    assert saved_paper.title == paper_data["title"]
    assert saved_paper.abstract == paper_data["abstract"]
    assert saved_paper.link == paper_data["link"]
    assert saved_paper.published == datetime.fromisoformat(paper_data["published"])
    assert saved_paper.keyword == keyword

    # Verify paper exists in database
    paper_in_db = db_session.query(Paper).filter_by(title="Test Paper").first()
    assert paper_in_db is not None
    assert paper_in_db.keyword == keyword

def test_save_paper_missing_fields(db_session):
    # Test with missing fields (should still save with defaults or fail gracefully)
    paper_data = {
        "title": "Incomplete Paper",
        "abstract": "",  # Empty abstract
        "link": "http://example.com/incomplete.pdf",
        "published": "2023-10-01T00:00:00"
    }
    keyword = "incomplete"

    saved_paper = save_paper(db_session, paper_data, keyword)
    assert saved_paper.title == paper_data["title"]
    assert saved_paper.abstract == ""
    assert saved_paper.keyword == keyword

def test_get_papers_by_keyword(db_session):
    # Save multiple papers
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

    # Retrieve papers
    retrieved_papers = get_papers_by_keyword(db_session, keyword, limit=10)
    
    # Verify results
    assert len(retrieved_papers) == 2
    assert retrieved_papers[0].title == "Paper 1"
    assert retrieved_papers[1].title == "Paper 2"
    assert retrieved_papers[0].keyword == keyword

def test_get_papers_by_keyword_no_results(db_session):
    # Test retrieving papers with non-existent keyword
    papers = get_papers_by_keyword(db_session, "nonexistent", limit=10)
    assert len(papers) == 0
