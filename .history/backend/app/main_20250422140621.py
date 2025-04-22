from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .services.arxiv import ArxivCrawler
from .database.crud import save_paper, get_papers_by_keyword, get_db

app = FastAPI()
crawler = ArxivCrawler(max_results=5)

@app.get("/search")
async def search(keyword: str, db: Session = Depends(get_db)):
    results = crawler.search_papers(keyword)
    saved_papers = []
    for paper in results:
        saved_paper = save_paper(db, paper, keyword)
        saved_papers.append(saved_paper)
    return {"results": [{"title": p.title, "abstract": p.abstract, "link": p.link, "published": p.published} for p in saved_papers]}

@app.get("/papers")
async def get_papers(keyword: str, db: Session = Depends(get_db)):
    papers = get_papers_by_keyword(db, keyword)
    return {
        "papers": [{
            "title": p.title,
            "abstract": p.abstract,
            "link": p.link,
            "published": p.published,
            "keywords": p.keywords.split(",") if p.keywords else [],
            "summary": p.summary
        } for p in papers]
    }