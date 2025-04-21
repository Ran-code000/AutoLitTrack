from sqlalchemy.orm import Session
from .models import Paper, SessionLocal
from datetime import datetime

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def save_paper(db: Session, paper: dict, keyword: str):
    db_paper = Paper(
        title=paper["title"],
        abstract=paper["abstract"],
        link=paper["link"],
        published=datetime.fromisoformat(paper["published"].replace("Z", "")),
        keyword=keyword
    )
    db.add(db_paper)
    db.commit()
    db.refresh(db_paper)
    return db_paper

def get_papers_by_keyword(db: Session, keyword: str, limit: int = 10):
    return db.query(Paper).filter(Paper.keyword == keyword).limit(limit).all()