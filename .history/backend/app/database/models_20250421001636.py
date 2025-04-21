# [1] SQLAlchemy核心组件导入
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
# √ create_engine: 数据库连接引擎
# √ Column: 字段定义基类
# √ Integer/String/Text/DateTime: 字段数据类型
# ! 注意：Text是可变长度文本，String需指定长度

# [2] ORM基础工具导入
from sqlalchemy.ext.declarative import declarative_base
# √ 获取声明式基类，用于模型继承
from sqlalchemy.orm import sessionmaker
# √ 创建数据库会话工厂
import datetime
# √ 提供DateTime字段的Python原生支持

# [3] 声明式基类初始化
Base = declarative_base()
# √ 所有模型类的父类
# ! 内存占用：~0.5MB (存储元数据)

# [4] 论文数据模型定义
class Paper(Base):
    __tablename__ = "papers"  # √ 物理表名
    
    # 字段定义
    id = Column(Integer, primary_key=True, index=True)
    # √ 自增主键，index加速查询
    title = Column(String(200), nullable=False)
    # √ 论文标题，长度限制200字符
    abstract = Column(Text, nullable=False)
    # √ 论文摘要，Text类型支持长文本
    link = Column(String(500), nullable=False)
    # √ 论文链接，长度限制500字符
    published = Column(DateTime, nullable=False)
    # √ 发布时间，存储为datetime对象
    keyword = Column(String(50), nullable=False, index=True)
    # √ 搜索关键词，添加索引加速查询

# [5] 数据库连接配置
DATABASE_URL = "sqlite:///papers.db"
# √ SQLite连接URL，相对路径
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    pool_size=5  # √ 连接池大小
)
# ! 生产环境应使用绝对路径

# [6] 会话工厂配置
SessionLocal = sessionmaker(
    autocommit=False,  # √ 关闭自动提交
    autoflush=False,   # √ 关闭自动flush
    bind=engine        # √ 绑定引擎
)

# [7] 表结构初始化
Base.metadata.create_all(bind=engine)
# √ 创建所有定义的表
# ! 注意：不会更新已有表结构