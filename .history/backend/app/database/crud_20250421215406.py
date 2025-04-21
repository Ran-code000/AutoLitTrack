from sqlalchemy.orm import Session
from .models import Paper
from .config import get_db, SessionLocal  # Import from config
from datetime import datetime

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def save_paper(db: Session, paper: dict, keyword: str):
    """
    Save a paper to the database, including keywords and summary.
    """
    db_paper = Paper(
        title=paper["title"],
        abstract=paper["abstract"],
        link=paper["link"],
        published=datetime.fromisoformat(paper["published"].replace("Z", "")),
        keyword=keyword,
        # keywords=",".join(paper.get("keywords", [])) if paper.get("keywords") else "",
        # summary=paper.get("summary", "")
    )
    db.add(db_paper)
    db.commit()
    db.refresh(db_paper)
    return db_paper

def get_papers_by_keyword(db: Session, keyword: str, limit: int = 10):
    """
    Retrieve papers by keyword.
    """
    return db.query(Paper).filter(Paper.keyword == keyword).limit(limit).all()