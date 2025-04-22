# database.py
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base
import datetime
from .config import engine  # Import engine from config

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
    keywords = Column(Text)  # Store keywords as comma-separated string
    summary = Column(Text)   # Store generated summary

# Create tables
Base.metadata.create_all(bind=engine) 