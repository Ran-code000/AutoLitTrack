# database.py
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

class Paper(Base):
    """Research paper database model"""
    __tablename__ = "papers"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    abstract = Column(Text, nullable=False)
    link = Column(String, nullable=False)
    published = Column(DateTime, nullable=False)
    keyword = Column(String, nullable=False)

# Database configuration
DATABASE_URL = "sqlite:///papers.db"
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Create tables
Base.metadata.create_all(bind=engine)