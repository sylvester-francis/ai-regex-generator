"""
API routes for regex generation
"""
import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.schemas import RegexGenerateRequest, RegexGenerateResponse
from app.services.ai_service import generate_regex_with_ai
from app.services.regex_service import test_regex
from app.services.db_service import create_pattern, create_request, create_test_case

# Initialize router
router = APIRouter()

# Initialize logger
logger = logging.getLogger(__name__)

@router.post("/generate", response_model=RegexGenerateResponse)
async def generate_regex(
    request: RegexGenerateRequest,
    db: AsyncSession = Depends(get_session)
):
    """
    Generate a regex pattern using AI based on the provided information
    """
    try:
        # Generate regex with AI
        result = await generate_regex_with_ai(
            request.description,
            request.sample_text,
            request.expected_matches
        )
        
        # Create regex request in database
        db_request = await create_request(
            db,
            description=request.description,
            sample_text=request.sample_text,
            expected_matches=request.expected_matches
        )
        
        # Create pattern name
        pattern_name = request.description[:50] + "..." if len(request.description) > 50 else request.description
        
        # Create pattern in database
        db_pattern = await create_pattern(
            db,
            name=pattern_name,
            pattern=result["pattern"],
            sample_text=request.sample_text,
            description=result["explanation"]
        )
        
        # Update request with pattern ID
        db_request.result_pattern_id = db_pattern.id
        db.add(db_request)
        await db.commit()
        
        # Create test cases
        for test_case in result.get("test_cases", []):
            if isinstance(test_case, dict) and "text" in test_case and "should_match" in test_case:
                await create_test_case(
                    db,
                    regex_pattern_id=db_pattern.id,
                    test_text=test_case["text"],
                    should_match=test_case["should_match"]
                )
        
        # Test the pattern against the sample text
        test_result = await test_regex(
            result["pattern"],
            request.sample_text,
            result.get("flags", "")
        )
        
        # Return response
        return RegexGenerateResponse(
            status="success",
            pattern=result["pattern"],
            pattern_id=db_pattern.id,
            explanation=result["explanation"],
            test_result=test_result,
            flags=result.get("flags", "")
        )
    
    except Exception as e:
        logger.exception("Error generating regex")
        return RegexGenerateResponse(
            status="error",
            message=str(e)
        )