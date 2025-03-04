"""
SQLAlchemy ORM models for the application
"""
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database import Base

class RegexPattern(Base):
    """Model for storing regex patterns"""
    __tablename__ = "regex_patterns"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    pattern: Mapped[str] = mapped_column(Text)
    sample_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    test_cases: Mapped[List["TestCase"]] = relationship("TestCase", back_populates="regex_pattern", cascade="all, delete-orphan")
    requests: Mapped[List["RegexRequest"]] = relationship("RegexRequest", back_populates="result_pattern")
    
    def __repr__(self) -> str:
        return f"<RegexPattern id={self.id} name={self.name}>"

class RegexRequest(Base):
    """Model for storing regex generation requests"""
    __tablename__ = "regex_requests"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(Text)
    sample_text: Mapped[str] = mapped_column(Text)
    expected_matches: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Foreign keys
    result_pattern_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("regex_patterns.id"), nullable=True)
    
    # Relationships
    result_pattern: Mapped[Optional[RegexPattern]] = relationship("RegexPattern", back_populates="requests")
    
    def __repr__(self) -> str:
        return f"<RegexRequest id={self.id}>"

class TestCase(Base):
    """Model for storing test cases for regex patterns"""
    __tablename__ = "test_cases"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    test_text: Mapped[str] = mapped_column(Text)
    should_match: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Foreign keys
    regex_pattern_id: Mapped[int] = mapped_column(Integer, ForeignKey("regex_patterns.id"))
    
    # Relationships
    regex_pattern: Mapped[RegexPattern] = relationship("RegexPattern", back_populates="test_cases")
    
    def __repr__(self) -> str:
        return f"<TestCase id={self.id} should_match={self.should_match}>"