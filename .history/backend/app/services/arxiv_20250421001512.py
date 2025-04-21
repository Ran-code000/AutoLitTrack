import requests  # √ HTTP请求库，用于调用arXiv API
from typing import List, Dict  # √ 类型注解支持
from xml.etree import ElementTree as ET  # √ XML解析工具
from urllib.parse import quote  # √ URL编码工具
from ..database.crud import save_paper, get_db, get_papers_by_keyword  # √ 导入数据库操作函数
from ..database.models import SessionLocal  # √ 导入会话工厂

class ArxivCrawler:
    BASE_URL = "http://export.arxiv.org/api/query"  # √ arXiv API端点
    
    def __init__(self, max_results: int = 5):
        self.max_results = max_results  # √ 控制单次请求返回数量
    def search_papers(self, keyword: str) -> List[Dict]:
    # URL编码处理
    query = quote(keyword)  # √ 处理特殊字符（如空格→%20）
    url = f"{self.BASE_URL}?search_query=all:{query}&start=0&max_results={self.max_results}"
    # √ 构造完整API请求URL
    
    try:
        # HTTP请求处理
        response = requests.get(url, timeout=10)  # √ 设置10秒超时
        response.raise_for_status()  # √ 自动处理4xx/5xx错误
        
        # XML解析
        root = ET.fromstring(response.content)  # √ 解析Atom格式XML
        papers = []
        
        # 数据提取
        for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
            paper = {
                "title": entry.find("{http://www.w3.org/2005/Atom}title").text.strip(),
                "abstract": entry.find("{http://www.w3.org/2005/Atom}summary").text.strip(),
                "link": entry.find("{http://www.w3.org/2005/Atom}id").text.strip(),
                "published": entry.find("{http://www.w3.org/2005/Atom}published").text.strip()
            }
            papers.append(paper)
        
        return papers  # √ 返回标准化数据字典列表
    
    # 异常处理
    except requests.exceptions.RequestException as e:
        print(f"Error fetching arXiv data: {e}")  # √ 网络请求错误
        return []  # 降级返回空列表
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")  # √ XML解析错误
        return []
        
# 测试用例（直接运行）
if __name__ == "__main__":
    """主程序入口（测试用）"""
    
    # 1. 初始化爬虫实例
    crawler = ArxivCrawler(max_results=3)  # 限制每次最多获取3篇论文
    
    # 2. 执行搜索（关键词："machine learning"）
    results = crawler.search_papers("machine learning")  # 返回论文结果列表
    
    # 3. 处理搜索结果
    if save_paper:  # 检查数据库存储功能是否可用
        try:
            # 3.1 获取数据库会话
            db = next(get_db())  # 从生成器获取SQLAlchemy会话
            
            # 3.2 遍历保存论文
            for paper in results:
                # 将每篇论文存入数据库
                saved_paper = save_paper(
                    db=db, 
                    paper=paper, 
                    keyword="machine learning"  # 记录搜索关键词
                )
                # 打印保存成功的论文标题
                print(f"已保存: {saved_paper.title}")
                
        except Exception as e:
            # 3.3 处理数据库异常
            print(f"数据库保存失败: {e}")
            # 注意：实际生产环境应添加事务回滚 (db.rollback())
    else:
        # 4. 无数据库时的处理方案
        for paper in results:
            # 4.1 打印论文基本信息
            print(f"标题: {paper['title']}")
            # 4.2 截取摘要前100字符（避免控制台输出过长）
            print(f"摘要: {paper['abstract'][:100]}...")  
            print(f"原文链接: {paper['link']}")
            # 4.3 显示标准化后的发布时间（ISO格式）
            print(f"发布时间: {paper['published']}")  
            print("---" * 20)  # 分隔线