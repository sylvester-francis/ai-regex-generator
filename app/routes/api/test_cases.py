"""
API routes for test cases
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.schemas import TestCaseCreate, TestCaseResponse
from app.services.db_service import create_test_case, get_pattern, delete_test_case

# Initialize router
router = APIRouter()

# Initialize logger
logger = logging.getLogger(__name__)

@router.post("", response_model=TestCaseResponse)
async def create_new_test_case(
    test_case: TestCaseCreate,
    pattern_id: int,
    db: AsyncSession = Depends(get_session)
):
    """
    Create a new test case for a pattern
    """
    try:
        # Check if pattern exists
        pattern = await get_pattern(db, pattern_id)
        if pattern is None:
            raise HTTPException(status_code=404, detail="Pattern not found")
        
        db_test_case = await create_test_case(
            db,
            regex_pattern_id=pattern_id,
            test_text=test_case.test_text,
            should_match=test_case.should_match
        )
        return db_test_case
    
    except HTTPException:
        raise
    
    except Exception as e:
        logger.exception("Error creating test case")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{test_case_id}")
async def delete_test_case_endpoint(
    test_case_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_session)
):
    """
    Delete a test case
    """
    try:
        deleted = await delete_test_case(db, test_case_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Test case not found")
        return {"message": "Test case deleted successfully"}
    
    except HTTPException:
        raise
    
    except Exception as e:
        logger.exception("Error deleting test case")
        raise HTTPException(status_code=500, detail=str(e))