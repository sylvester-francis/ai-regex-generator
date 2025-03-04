"""
API route initialization
"""
from fastapi import APIRouter
from .api import (
    regex_generation,
    regex_testing,
    patterns,
    test_cases
)

# Create main router
router = APIRouter()

# Include all API routes
router.include_router(regex_generation.router, prefix="/regex", tags=["regex-generation"])
router.include_router(regex_testing.router, prefix="/regex", tags=["regex-testing"])
router.include_router(patterns.router, prefix="/patterns", tags=["patterns"])
router.include_router(test_cases.router, prefix="/test-cases", tags=["test-cases"])

__all__ = ["router"]