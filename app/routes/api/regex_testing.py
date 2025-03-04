"""
API routes for regex testing
"""
import logging
from fastapi import APIRouter, HTTPException

from app.schemas import RegexTestRequest, RegexTestResponse
from app.services.regex_service import test_regex

# Initialize router
router = APIRouter()

# Initialize logger
logger = logging.getLogger(__name__)

@router.post("/test", response_model=RegexTestResponse)
async def test_regex_endpoint(request: RegexTestRequest):
    """
    Test a regex pattern against text and return match information
    """
    try:
        # Test the pattern
        result = await test_regex(
            request.pattern,
            request.test_text,
            request.flags
        )
        
        # Return response
        return RegexTestResponse(
            status="success",
            result=result
        )
    
    except Exception as e:
        logger.exception("Error testing regex")
        return RegexTestResponse(
            status="error",
            message=str(e)
        )

@router.get("/flags")
async def get_flags():
    """
    Get information about available regex flags
    """
    from app.services.regex_service import get_flag_descriptions
    return get_flag_descriptions()