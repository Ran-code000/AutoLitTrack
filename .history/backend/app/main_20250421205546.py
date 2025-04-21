from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .services.arxiv import ArxivCrawler
from .services.nlp import NLPProcessor
from .database.crud import save_paper, get_papers_by_keyword, get_db


app = FastAPI()
crawler = ArxivCrawler(max_results=5)
nlp = NLPProcessor()

@app.get("/search")
async def search(keyword: str, db: Session = Depends(get_db)):
    """
    Search arXiv papers, extract keywords, generate summaries, and save to database.
    """
    results = crawler.search_papers(keyword)
    processed_results = []
    for paper in results:
        # # Extract keywords and generate summary
        # keywords = nlp.extract_keywords(paper["abstract"])
        # summary = nlp.generate_summary(paper["abstract"])
        # # Add to paper dict
        # paper["keywords"] = keywords
        # paper["summary"] = summary
        # Save to database
        saved_paper = save_paper(db, paper, keyword)
        processed_results.append({
            "title": saved_paper.title,
            "abstract": saved_paper.abstract,
            "link": saved_paper.link,
            "published": saved_paper.published
            # "keywords": saved_paper.keywords.split(",") if saved_paper.keywords else [],
            # "summary": saved_paper.summary
        })
    return {"results": processed_results}

@app.get("/papers")
async def get_papers(keyword: str, db: Session = Depends(get_db)):
    """
    Retrieve papers by keyword from database.
    """
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