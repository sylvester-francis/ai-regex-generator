"""
Unit tests for regex service
"""
import pytest
from app.services.regex_service import test_regex


@pytest.mark.asyncio
async def test_basic_matching():
    """Test basic regex matching"""
    # Test a simple pattern
    result = await test_regex(r"\d+", "There are 123 items")
    
    assert result["success"] is True
    assert result["match_count"] == 1
    assert len(result["matches"]) == 1
    assert result["matches"][0]["full_match"] == "123"


@pytest.mark.asyncio
async def test_capturing_groups():
    """Test regex with capturing groups"""
    # Test a pattern with groups
    result = await test_regex(r"(\w+)@(\w+)\.(\w+)", "Contact me at user@example.com")
    
    assert result["success"] is True
    assert result["match_count"] == 1
    
    match = result["matches"][0]
    assert match["full_match"] == "user@example.com"
    assert len(match["groups"]) == 3
    assert match["groups"][0]["content"] == "user"
    assert match["groups"][1]["content"] == "example"
    assert match["groups"][2]["content"] == "com"


@pytest.mark.asyncio
async def test_multiple_matches():
    """Test regex with multiple matches"""
    # Test a pattern that matches multiple times
    result = await test_regex(r"\b\w{3}\b", "The cat sat on the mat")
    
    assert result["success"] is True
    assert result["match_count"] == 3
    assert [m["full_match"] for m in result["matches"]] == ["The", "cat", "sat"]


@pytest.mark.asyncio
async def test_no_matches():
    """Test regex with no matches"""
    # Test a pattern that doesn't match
    result = await test_regex(r"\d+", "No numbers here")
    
    assert result["success"] is True
    assert result["match_count"] == 0
    assert len(result["matches"]) == 0


@pytest.mark.asyncio
async def test_invalid_pattern():
    """Test with invalid regex pattern"""
    # Test an invalid pattern
    result = await test_regex(r"[a-z", "This should fail")
    
    assert result["success"] is False
    assert "error" in result


@pytest.mark.asyncio
async def test_with_flags():
    """Test regex with flags"""
    # Test case-insensitive flag
    result = await test_regex(r"test", "This is a TEST", "i")
    
    assert result["success"] is True
    assert result["match_count"] == 1
    assert result["matches"][0]["full_match"] == "TEST"
    
    # Test without flag (should not match)
    result = await test_regex(r"test", "This is a TEST")
    
    assert result["success"] is True
    assert result["match_count"] == 0