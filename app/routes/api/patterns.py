"""
API routes for regex patterns
"""
import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.schemas import (
    RegexPatternCreate,
    RegexPatternResponse,
    TestCaseResponse
)
from app.services.db_service import (
    create_pattern,
    get_pattern,
    get_patterns,
    update_pattern,
    delete_pattern,
    get_test_cases
)

# Initialize router
router = APIRouter()

# Initialize logger
logger = logging.getLogger(__name__)

@router.post("", response_model=RegexPatternResponse)
async def create_regex_pattern(
    pattern: RegexPatternCreate,
    db: AsyncSession = Depends(get_session)
):
    """
    Create a new regex pattern
    """
    try:
        db_pattern = await create_pattern(
            db,
            name=pattern.name,
            pattern=pattern.pattern,
            sample_text=pattern.sample_text,
            description=pattern.description
        )
        return db_pattern
    
    except Exception as e:
        logger.exception("Error creating pattern")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("", response_model=List[RegexPatternResponse])
async def read_patterns(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_session)
):
    """
    Get all regex patterns with pagination
    """
    try:
        patterns = await get_patterns(db, skip=skip, limit=limit)
        return patterns
    
    except Exception as e:
        logger.exception("Error getting patterns")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{pattern_id}", response_model=RegexPatternResponse)
async def read_pattern(
    pattern_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_session)
):
    """
    Get a regex pattern by ID
    """
    try:
        pattern = await get_pattern(db, pattern_id)
        if pattern is None:
            raise HTTPException(status_code=404, detail="Pattern not found")
        return pattern
    
    except HTTPException:
        raise
    
    except Exception as e:
        logger.exception("Error getting pattern")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{pattern_id}", response_model=RegexPatternResponse)
async def update_regex_pattern(
    pattern: RegexPatternCreate,
    pattern_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_session)
):
    """
    Update a regex pattern
    """
    try:
        updated_pattern = await update_pattern(
            db,
            pattern_id=pattern_id,
            name=pattern.name,
            pattern=pattern.pattern,
            sample_text=pattern.sample_text,
            description=pattern.description
        )
        if updated_pattern is None:
            raise HTTPException(status_code=404, detail="Pattern not found")
        return updated_pattern
    
    except HTTPException:
        raise
    
    except Exception as e:
        logger.exception("Error updating pattern")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{pattern_id}")
async def delete_regex_pattern(
    pattern_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_session)
):
    """
    Delete a regex pattern
    """
    try:
        deleted = await delete_pattern(db, pattern_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Pattern not found")
        return {"message": "Pattern deleted successfully"}
    
    except HTTPException:
        raise
    
    except Exception as e:
        logger.exception("Error deleting pattern")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{pattern_id}/test-cases", response_model=List[TestCaseResponse])
async def read_pattern_test_cases(
    pattern_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_session)
):
    """
    Get all test cases for a pattern
    """
    try:
        # Check if pattern exists
        pattern = await get_pattern(db, pattern_id)
        if pattern is None:
            raise HTTPException(status_code=404, detail="Pattern not found")
        
        test_cases = await get_test_cases(db, pattern_id)
        return test_cases
    
    except HTTPException:
        raise
    
    except Exception as e:
        logger.exception("Error getting test cases")
        raise HTTPException(status_code=500, detail=str(e))