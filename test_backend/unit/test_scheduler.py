import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from backend.app.services.scheduler import Scheduler
from backend.app.database.models import Base, Paper
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.mark.asyncio
async def test_fetch_and_save_papers(db_session):
    # Mock ArxivCrawler
    scheduler = Scheduler()
    mock_papers = [
        {
            "title": "Test Paper",
            "abstract": "Test abstract",
            "link": "http://example.com/test.pdf",
            "published": "2023-10-01T00:00:00"
        }
    ]
    with patch.object(scheduler.crawler, "search_papers", Mock(return_value=mock_papers)):
        # Mock get_db
        with patch("backend.app.services.scheduler.get_db", return_value=iter([db_session])):
            await scheduler.fetch_and_save_papers(keyword="test")

    # Verify paper saved
    paper_in_db = db_session.query(Paper).filter_by(title="Test Paper").first()
    assert paper_in_db is not None
    assert paper_in_db.keyword == "test"
    assert paper_in_db.abstract == "Test abstract"

@pytest.mark.asyncio
async def test_fetch_and_save_papers_failure(db_session):
    # Mock ArxivCrawler to raise an exception
    scheduler = Scheduler()
    with patch.object(scheduler.crawler, "search_papers", side_effect=Exception("API error")):
        # Mock get_db
        with patch("backend.app.services.scheduler.get_db", return_value=iter([db_session])):
            await scheduler.fetch_and_save_papers(keyword="test")

    # Verify no papers saved
    papers = db_session.query(Paper).all()
    assert len(papers) == 0, "No papers should be saved when search_papers fails"

@pytest.mark.asyncio
async def test_schedule_tasks():
    scheduler = Scheduler()
    with patch("apscheduler.schedulers.asyncio.AsyncIOScheduler.add_job") as mock_add_job:
        scheduler.schedule_tasks()
        mock_add_job.assert_called_once()
        call_args = mock_add_job.call_args
        assert call_args.kwargs["id"] == "daily_fetch_papers"
        assert call_args.kwargs["kwargs"] == {"keyword": "machine learning"}