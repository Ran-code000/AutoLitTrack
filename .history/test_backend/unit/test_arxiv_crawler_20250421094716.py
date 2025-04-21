import pytest
from unittest.mock import patch, MagicMock
from backend.app.services.arxiv import ArxivCrawler

# 测试数据模拟
SAMPLE_XML_RESPONSE = """
<feed xmlns="http://www.w3.org/2005/Atom">
    <entry>
        <title>Test Paper Title</title>
        <summary>Test abstract content</summary>
        <id>http://arxiv.org/abs/1234.56789</id>
        <published>2023-01-01T00:00:00Z</published>
    </entry>
</feed>
"""

class TestArxivCrawler:
    @patch('requests.get')
    def test_search_papers_success(self, mock_get):
        # 配置mock响应
        mock_response = MagicMock()
        mock_response.content = SAMPLE_XML_RESPONSE
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # 测试执行
        crawler = ArxivCrawler(max_results=1)
        results = crawler.search_papers("machine learning")
        
        # 验证结果
        assert len(results) == 1
        assert results[0]["title"] == "Test Paper Title"
        assert results[0]["link"] == "http://arxiv.org/abs/1234.56789"
    
    @patch('requests.get')
    def test_search_papers_failure(self, mock_get):
        # 模拟请求异常
        mock_get.side_effect = Exception("Network error")
        
        crawler = ArxivCrawler()
        results = crawler.search_papers("machine learning")
        
        assert len(results) == 0

    def test_max_results_parameter(self):
        crawler = ArxivCrawler(max_results=10)
        assert crawler.max_results == 10