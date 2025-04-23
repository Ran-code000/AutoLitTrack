import pytest
from unittest.mock import patch, Mock
from backend.app.services.arxiv import ArxivCrawler
from sqlalchemy import text
import requests

@pytest.fixture
def crawler():
    return ArxivCrawler(max_results=3)

def test_search_papers_success(crawler):
    # Mock API response
    mock_response = Mock()
    mock_response.status_code = 200
    xml_data = """
    <feed xmlns="http://www.w3.org/2005/Atom">
        <entry>
            <id>http://arxiv.org/abs/1234.5678</id>
            <title>Test Paper 1</title>
            <summary>Test abstract 1</summary>
            <published>2023-10-01T00:00:00Z</published>
        </entry>
        <entry>
            <id>http://arxiv.org/abs/1234.5679</id>
            <title>Test Paper 2</title>
            <summary>Test abstract 2</summary>
            <published>2023-10-02T00:00:00Z</published>
        </entry>
    </feed>
    """
    mock_response.content = xml_data.encode('utf-8')
    mock_response.raise_for_status = Mock()

    with patch("requests.get", return_value=mock_response) as mock_get:
        results = crawler.search_papers("machine learning")
        
        assert isinstance(results, list)
        assert len(results) == 2
        assert mock_get.called
        
        paper = results[0]
        assert paper["title"] == "Test Paper 1"
        assert paper["abstract"] == "Test abstract 1"
        assert paper["link"] == "http://arxiv.org/abs/1234.5678"
        assert paper["published"] == "2023-10-01T00:00:00Z"
        assert isinstance(paper["title"], str)
        assert isinstance(paper["abstract"], str)
        assert isinstance(paper["link"], str)
        assert isinstance(paper["published"], str)

def test_search_papers_empty_keyword(crawler):
    # Mock API response for empty keyword
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = b"<feed xmlns='http://www.w3.org/2005/Atom'></feed>"
    mock_response.raise_for_status = Mock()

    with patch("requests.get", return_value=mock_response) as mock_get:
        results = crawler.search_papers("")
        
        assert isinstance(results, list)
        assert len(results) == 0
        assert not mock_get.called  # Empty keyword skips API call

def test_search_papers_invalid_keyword(crawler):
    # Mock API response for invalid keyword
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = b"<feed xmlns='http://www.w3.org/2005/Atom'></feed>"
    mock_response.raise_for_status = Mock()

    with patch("requests.get", return_value=mock_response) as mock_get:
        results = crawler.search_papers("invalid_keyword_with_no_results_12345")
        
        assert isinstance(results, list)
        assert len(results) == 0
        assert mock_get.called

def test_search_papers_api_error(crawler):
    # Mock API error
    with patch("requests.get") as mock_get:
        mock_get.side_effect = requests.RequestException("API error")
        results = crawler.search_papers("machine learning")
        
        assert isinstance(results, list)
        assert len(results) == 0
        assert mock_get.called

def test_search_papers_invalid_xml(crawler):
    # Mock invalid XML response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = b"<invalid>xml</invalid>"
    mock_response.raise_for_status = Mock()

    with patch("requests.get", return_value=mock_response) as mock_get:
        results = crawler.search_papers("machine learning")
        
        assert isinstance(results, list)
        assert len(results) == 0
        assert mock_get.called

def test_search_papers_timeout():
    with patch("requests.get", side_effect=requests.Timeout("Request timed out")):
        crawler = ArxivCrawler(max_results=5)
        results = crawler.search_papers("test")
        assert results == []



def test_search_papers_http_403_error(crawler):
    mock_response = Mock()
    mock_response.status_code = 403
    mock_response.content = b"<feed xmlns='http://www.w3.org/2005/Atom'></feed>"
    mock_response.raise_for_status = Mock(side_effect=requests.HTTPError("403 Forbidden"))

    with patch("requests.get", return_value=mock_response) as mock_get:
        results = crawler.search_papers("machine learning")
        
        assert isinstance(results, list)
        assert len(results) == 0
        assert mock_get.called

def test_search_papers_non_ascii_keyword(crawler):
    mock_response = Mock()
    mock_response.status_code = 200
    xml_data = """
    <feed xmlns="http://www.w3.org/2005/Atom">
        <entry>
            <id>http://arxiv.org/abs/1234.5678</id>
            <title>中文论文</title>
            <summary>测试摘要</summary>
            <published>2023-10-01T00:00:00Z</published>
        </entry>
    </feed>
    """
    mock_response.content = xml_data.encode('utf-8')
    mock_response.raise_for_status = Mock()

    with patch("requests.get", return_value=mock_response) as mock_get:
        results = crawler.search_papers("机器学习")
        
        assert isinstance(results, list)
        assert len(results) == 1
        assert mock_get.called
        paper = results[0]
        assert paper["title"] == "中文论文"
        assert paper["abstract"] == "测试摘要"

def test_search_papers_invalid_max_results():
    crawler = ArxivCrawler(max_results=0)
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = b"<feed xmlns='http://www.w3.org/2005/Atom'></feed>"
    mock_response.raise_for_status = Mock()

    with patch("requests.get", return_value=mock_response) as mock_get:
        results = crawler.search_papers("machine learning")
        
        assert isinstance(results, list)
        assert len(results) == 0
        assert mock_get.called