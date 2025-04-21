import requests
from typing import List, Dict
from xml.etree import ElementTree as ET
from urllib.parse import quote


class ArxivCrawler:
    BASE_URL = "https://export.arxiv.org/api/query"
    
    def __init__(self, max_results: int = 5):
        self.max_results = max_results
    
    def search_papers(self, keyword: str) -> List[Dict]:
        """
        Search arXiv papers by keyword using the arXiv API.
        Returns a list of dictionaries containing paper details.
        """
        # Encode keyword for URL
        query = quote(keyword)
        url = f"{self.BASE_URL}?search_query=all:{query}&start=0&max_results={self.max_results}"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Raise exception for bad status codes
            
            # Parse XML response
            root = ET.fromstring(response.content)
            papers = []
            
            for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
                paper = {
                    "title": entry.find("{http://www.w3.org/2005/Atom}title").text.strip(),
                    "abstract": entry.find("{http://www.w3.org/2005/Atom}summary").text.strip(),
                    "link": entry.find("{http://www.w3.org/2005/Atom}id").text.strip(),
                    "published": entry.find("{http://www.w3.org/2005/Atom}published").text.strip()
                }
                papers.append(paper)
            
            return papers
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching arXiv data: {e}")
            return []
        except ET.ParseError as e:
            print(f"Error parsing XML: {e}")
            return []

# Example usage (for testing)
if __name__ == "__main__":  
    crawler = ArxivCrawler(max_results=3)
    results = crawler.search_papers("machine learning")
    

    for paper in results:
        print(f"Title: {paper['title']}")
        print(f"Abstract: {paper['abstract'][:100]}...")
        print(f"Link: {paper['link']}")
        print(f"Published: {paper['published']}")  # Added published field
        print("---" * 20)