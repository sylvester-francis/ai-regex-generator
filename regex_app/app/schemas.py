"""
Pydantic models for request/response validation
"""
from datetime import datetime
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field

# Base schemas
class TestCaseBase(BaseModel):
    """Base schema for test cases"""
    test_text: str
    should_match: bool = True

class RegexPatternBase(BaseModel):
    """Base schema for regex patterns"""
    name: str
    pattern: str
    sample_text: Optional[str] = None
    description: Optional[str] = None

class RegexRequestBase(BaseModel):
    """Base schema for regex generation requests"""
    description: str
    sample_text: str
    expected_matches: Optional[str] = None

# Create schemas
class TestCaseCreate(TestCaseBase):
    """Schema for creating test cases"""
    pass

class RegexPatternCreate(RegexPatternBase):
    """Schema for creating regex patterns"""
    pass

class RegexRequestCreate(RegexRequestBase):
    """Schema for creating regex generation requests"""
    pass

# Response schemas
class TestCaseResponse(TestCaseBase):
    """Schema for test case responses"""
    id: int
    regex_pattern_id: int
    
    class Config:
        from_attributes = True

class RegexPatternResponse(RegexPatternBase):
    """Schema for regex pattern responses"""
    id: int
    created_at: datetime
    updated_at: datetime
    test_cases: List[TestCaseResponse] = []
    
    class Config:
        from_attributes = True

class RegexRequestResponse(RegexRequestBase):
    """Schema for regex generation request responses"""
    id: int
    created_at: datetime
    result_pattern_id: Optional[int] = None
    
    class Config:
        from_attributes = True

# Specialized schemas
class RegexGenerateRequest(BaseModel):
    """Schema for regex generation request"""
    description: str = Field(..., description="Description of what the regex should do")
    sample_text: str = Field(..., description="Sample text containing examples of what to match")
    expected_matches: Optional[str] = Field(None, description="Specific parts of the sample text that should match")

class RegexTestRequest(BaseModel):
    """Schema for regex testing request"""
    pattern: str = Field(..., description="The regex pattern to test")
    test_text: str = Field(..., description="The text to test against")
    flags: str = Field("", description="Regex flags (i, m, s, x)")

class GroupMatch(BaseModel):
    """Schema for group match information"""
    group_num: int
    content: str
    start: int
    end: int

class Match(BaseModel):
    """Schema for match information"""
    full_match: str
    start: int
    end: int
    groups: List[GroupMatch] = []

class RegexTestResult(BaseModel):
    """Schema for regex test result"""
    success: bool
    match_count: Optional[int] = None
    matches: Optional[List[Match]] = None
    error: Optional[str] = None

class RegexGenerateResponse(BaseModel):
    """Schema for regex generation response"""
    status: str
    pattern: Optional[str] = None
    pattern_id: Optional[int] = None
    explanation: Optional[str] = None
    test_result: Optional[RegexTestResult] = None
    flags: Optional[str] = None
    message: Optional[str] = None

class RegexTestResponse(BaseModel):
    """Schema for regex test response"""
    status: str
    result: Optional[RegexTestResult] = None
    message: Optional[str] = None