import pytest
from ...backend.app.services.arxiv import ArxivCrawler

def test_search_papers_success():
    crawler = ArxivCrawler(max_results=3)
    results = crawler.search_papers("machine learning")
    
    assert isinstance(results, list)
    assert len(results) <= 3
    if results:
        paper = results[0]
        assert "title" in paper
        assert "abstract" in paper
        assert "link" in paper
        assert "published" in paper
        assert isinstance(paper["title"], str)
        assert isinstance(paper["abstract"], str)
        assert isinstance(paper["link"], str)
        assert isinstance(paper["published"], str)

def test_search_papers_empty_keyword():
    crawler = ArxivCrawler(max_results=3)
    results = crawler.search_papers("")
    
    assert isinstance(results, list)
    assert len(results) == 0

def test_search_papers_invalid_keyword():
    crawler = ArxivCrawler(max_results=3)
    results = crawler.search_papers("invalid_keyword_with_no_results_12345")
    
    assert isinstance(results, list)
    # May return empty or some results, but should not raise an error
    assert len(results) >= 0

# Manual test for console output (similar to original)
def test_print_papers():
    crawler = ArxivCrawler(max_results=3)
    results = crawler.search_papers("machine learning")
    
    for paper in results:
        print(f"Title: {paper['title']}")
        print(f"Abstract: {paper['abstract'][:100]}...")
        print(f"Link: {paper['link']}")
        print(f"Published: {paper['published']}")
        print("---" * 20)