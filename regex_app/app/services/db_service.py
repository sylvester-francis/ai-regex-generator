"""
Service for database operations
"""
import logging
from typing import List, Optional, Dict, Any
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import RegexPattern, RegexRequest, TestCase

# Initialize logger
logger = logging.getLogger(__name__)

# RegexPattern operations
async def create_pattern(
    db: AsyncSession,
    name: str,
    pattern: str,
    sample_text: Optional[str] = None,
    description: Optional[str] = None
) -> RegexPattern:
    """
    Create a new regex pattern
    
    Args:
        db: Database session
        name: Name of the pattern
        pattern: Regex pattern string
        sample_text: Sample text for testing
        description: Description or explanation
        
    Returns:
        Created RegexPattern instance
    """
    db_pattern = RegexPattern(
        name=name,
        pattern=pattern,
        sample_text=sample_text,
        description=description
    )
    db.add(db_pattern)
    await db.commit()
    await db.refresh(db_pattern)
    return db_pattern

async def get_pattern(db: AsyncSession, pattern_id: int) -> Optional[RegexPattern]:
    """
    Get a regex pattern by ID
    
    Args:
        db: Database session
        pattern_id: ID of the pattern
        
    Returns:
        RegexPattern instance or None if not found
    """
    query = select(RegexPattern).options(
        selectinload(RegexPattern.test_cases)
    ).where(RegexPattern.id == pattern_id)
    result = await db.execute(query)
    return result.scalars().first()

async def get_patterns(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[RegexPattern]:
    """
    Get all regex patterns with pagination
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        
    Returns:
        List of RegexPattern instances
    """
    query = select(RegexPattern).order_by(RegexPattern.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    return list(result.scalars().all())

async def update_pattern(
    db: AsyncSession,
    pattern_id: int,
    name: Optional[str] = None,
    pattern: Optional[str] = None,
    sample_text: Optional[str] = None,
    description: Optional[str] = None
) -> Optional[RegexPattern]:
    """
    Update a regex pattern
    
    Args:
        db: Database session
        pattern_id: ID of the pattern to update
        name: New name (if provided)
        pattern: New regex pattern (if provided)
        sample_text: New sample text (if provided)
        description: New description (if provided)
        
    Returns:
        Updated RegexPattern instance or None if not found
    """
    # Build update dictionary with only provided values
    update_data = {}
    if name is not None:
        update_data["name"] = name
    if pattern is not None:
        update_data["pattern"] = pattern
    if sample_text is not None:
        update_data["sample_text"] = sample_text
    if description is not None:
        update_data["description"] = description
        
    if not update_data:
        return await get_pattern(db, pattern_id)
    
    # Update the pattern
    query = update(RegexPattern).where(RegexPattern.id == pattern_id).values(**update_data)
    await db.execute(query)
    await db.commit()
    
    # Return the updated pattern
    return await get_pattern(db, pattern_id)

async def delete_pattern(db: AsyncSession, pattern_id: int) -> bool:
    """
    Delete a regex pattern
    
    Args:
        db: Database session
        pattern_id: ID of the pattern to delete
        
    Returns:
        True if deleted, False if not found
    """
    # Check if pattern exists
    pattern = await get_pattern(db, pattern_id)
    if not pattern:
        return False
    
    # Delete the pattern
    query = delete(RegexPattern).where(RegexPattern.id == pattern_id)
    await db.execute(query)
    await db.commit()
    return True

# RegexRequest operations
async def create_request(
    db: AsyncSession,
    description: str,
    sample_text: str,
    expected_matches: Optional[str] = None,
    result_pattern_id: Optional[int] = None
) -> RegexRequest:
    """
    Create a new regex generation request
    
    Args:
        db: Database session
        description: Description of what the regex should do
        sample_text: Sample text for testing
        expected_matches: Expected matches (if provided)
        result_pattern_id: ID of the resulting pattern (if available)
        
    Returns:
        Created RegexRequest instance
    """
    db_request = RegexRequest(
        description=description,
        sample_text=sample_text,
        expected_matches=expected_matches,
        result_pattern_id=result_pattern_id
    )
    db.add(db_request)
    await db.commit()
    await db.refresh(db_request)
    return db_request

async def get_request(db: AsyncSession, request_id: int) -> Optional[RegexRequest]:
    """
    Get a regex request by ID
    
    Args:
        db: Database session
        request_id: ID of the request
        
    Returns:
        RegexRequest instance or None if not found
    """
    query = select(RegexRequest).options(
        selectinload(RegexRequest.result_pattern)
    ).where(RegexRequest.id == request_id)
    result = await db.execute(query)
    return result.scalars().first()

# TestCase operations
async def create_test_case(
    db: AsyncSession,
    regex_pattern_id: int,
    test_text: str,
    should_match: bool = True
) -> TestCase:
    """
    Create a new test case
    
    Args:
        db: Database session
        regex_pattern_id: ID of the related pattern
        test_text: Test text
        should_match: Whether the pattern should match the test text
        
    Returns:
        Created TestCase instance
    """
    db_test_case = TestCase(
        regex_pattern_id=regex_pattern_id,
        test_text=test_text,
        should_match=should_match
    )
    db.add(db_test_case)
    await db.commit()
    await db.refresh(db_test_case)
    return db_test_case

async def get_test_cases(db: AsyncSession, pattern_id: int) -> List[TestCase]:
    """
    Get all test cases for a pattern
    
    Args:
        db: Database session
        pattern_id: ID of the pattern
        
    Returns:
        List of TestCase instances
    """
    query = select(TestCase).where(TestCase.regex_pattern_id == pattern_id)
    result = await db.execute(query)
    return list(result.scalars().all())

async def delete_test_case(db: AsyncSession, test_case_id: int) -> bool:
    """
    Delete a test case
    
    Args:
        db: Database session
        test_case_id: ID of the test case to delete
        
    Returns:
        True if deleted, False if not found
    """
    query = delete(TestCase).where(TestCase.id == test_case_id)
    result = await db.execute(query)
    await db.commit()
    return result.rowcount > 0