from sqlalchemy.orm import Session  # √ SQLAlchemy会话类型注解
from .models import Paper, SessionLocal  # √ 从本地模块导入模型和会话工厂
from datetime import datetime  # √ 日期时间转换工具

def get_db():
    """生成数据库会话的生成器函数"""
    db = SessionLocal()  # √ 创建新会话
    try:
        yield db  # √ 返回会话供使用
    finally:
        db.close()  # √ 确保会话最终关闭
# → FastAPI依赖注入系统会调用此生成器
# ! 每个请求必须独立会话

def save_paper(db: Session, paper: dict, keyword: str):
    """保存论文到数据库"""
    db_paper = Paper(
        title=paper["title"],  # √ 映射标题字段
        abstract=paper["abstract"],  # √ 映射摘要字段
        link=paper["link"],  # √ 映射链接字段
        published=datetime.fromisoformat(  # √ 日期格式转换
            paper["published"].replace("Z", "")  # √ 处理UTC时区标记
        ),
        keyword=keyword  # √ 记录搜索关键词
    )
    db.add(db_paper)  # √ 添加到会话
    db.commit()  # √ 提交事务
    db.refresh(db_paper)  # √ 刷新获取数据库生成值（如自增ID）
    return db_paper  # √ 返回带数据库状态的论文对象
# ! 注意：published字段需确保ISO格式输入

def get_papers_by_keyword(db: Session, keyword: str, limit: int = 10):
    """按关键词查询论文"""
    return (
        db.query(Paper)  # √ 构建查询
        .filter(Paper.keyword == keyword)  # √ 添加关键词过滤
        .limit(limit)  # √ 限制结果数量
        .all()  # √ 执行查询获取列表
    )
# → 返回List[Paper]对象
# ! 性能依赖keyword字段索引