from sqlalchemy.orm import Session
from .models import Paper
from .config import get_db, SessionLocal  # Import from config
from datetime import datetime

def save_paper(db: Session, paper: dict, keyword: str):
    """
    Save a paper to the database, including keywords and summary.
    """
    published = paper.get("published")
    if isinstance(published, str):
        try:
            published = datetime.fromisoformat(published.replace("Z", "+00:00"))
        except ValueError:
            published = None

    db_paper = Paper(
        title=paper.get("title"),
        abstract=paper.get("abstract"),
        link=paper.get("link"),
        published=published,
        keyword=keyword,
        keywords=",".join(paper.get("keywords", [])),
        summary=paper.get("summary", "")
    )
    db.add(db_paper)
    db.commit()
    db.refresh(db_paper)
    return db_paper

def get_papers_by_keyword(db: Session, keyword: str, limit: int = 10):
    """
    Retrieve papers by keyword.
    """
    return db.query(Paper).filter(Paper.keyword.ilike(f"%{keyword}%")).limit(limit).all() 