"""
Service for regex pattern testing and management
"""
import regex
import logging
from typing import Dict, Any, List, Optional

# Initialize logger
logger = logging.getLogger(__name__)

async def test_regex(pattern: str, text: str, flag_str: str = "") -> Dict[str, Any]:
    """
    Test a regex pattern against a text and return match information
    
    Args:
        pattern: The regex pattern to test
        text: The text to test against
        flag_str: String of regex flags (i, m, s, x)
        
    Returns:
        Dictionary with match information
    """
    try:
        # Parse flags
        flags = 0
        if 'i' in flag_str:
            flags |= regex.IGNORECASE
        if 'm' in flag_str:
            flags |= regex.MULTILINE
        if 's' in flag_str:
            flags |= regex.DOTALL
        if 'x' in flag_str:
            flags |= regex.VERBOSE
            
        # Compile regex
        regex_pattern = regex.compile(pattern, flags)
        
        # Find all matches
        matches = list(regex_pattern.finditer(text))
        
        # Prepare match information
        match_info = []
        for match in matches:
            match_data = {
                "full_match": match.group(0),
                "start": match.start(),
                "end": match.end(),
                "groups": []
            }
            
            # Add group information
            for i in range(1, len(match.groups()) + 1):
                if match.group(i) is not None:
                    match_data["groups"].append({
                        "group_num": i,
                        "content": match.group(i),
                        "start": match.start(i),
                        "end": match.end(i)
                    })
            
            match_info.append(match_data)
            
        return {
            "success": True,
            "match_count": len(matches),
            "matches": match_info
        }
        
    except Exception as e:
        logger.exception("Error testing regex")
        return {
            "success": False,
            "error": str(e)
        }

def get_flag_descriptions() -> List[Dict[str, str]]:
    """
    Get descriptions of available regex flags
    
    Returns:
        List of dictionaries with flag information
    """
    return [
        {"flag": "i", "name": "Case insensitive", "description": "Makes the regex case insensitive"},
        {"flag": "m", "name": "Multi-line", "description": "^ and $ match start/end of line, not just start/end of string"},
        {"flag": "s", "name": "Dot matches newline", "description": "Allows . to match newline characters"},
        {"flag": "x", "name": "Verbose", "description": "Allows whitespace and comments in the pattern"}
    ]

def explain_regex_component(component: str) -> Optional[str]:
    """
    Get an explanation for a regex component
    
    Args:
        component: The regex component to explain
        
    Returns:
        Explanation or None if not recognized
    """
    explanations = {
        "^": "Matches the start of the string",
        "$": "Matches the end of the string",
        ".": "Matches any character except newline",
        "\\d": "Matches a digit (0-9)",
        "\\D": "Matches a non-digit character",
        "\\w": "Matches a word character (alphanumeric + underscore)",
        "\\W": "Matches a non-word character",
        "\\s": "Matches a whitespace character",
        "\\S": "Matches a non-whitespace character",
        "\\b": "Matches a word boundary",
        "\\B": "Matches a non-word boundary",
        "*": "Matches 0 or more of the preceding element",
        "+": "Matches 1 or more of the preceding element",
        "?": "Matches 0 or 1 of the preceding element",
        "{m}": "Matches exactly m of the preceding element",
        "{m,}": "Matches m or more of the preceding element",
        "{m,n}": "Matches between m and n of the preceding element",
        "|": "Acts as an OR operator, matching either the expression before or after it",
        "()": "Creates a capture group",
        "(?:)": "Creates a non-capturing group",
        "(?=)": "Positive lookahead assertion",
        "(?!)": "Negative lookahead assertion",
        "(?<=)": "Positive lookbehind assertion",
        "(?<!)": "Negative lookbehind assertion",
        "[abc]": "Matches any character in the set (a, b, or c)",
        "[^abc]": "Matches any character not in the set (not a, b, or c)",
        "[a-z]": "Matches any character in the range (a through z)",
    }
    
    return explanations.get(component)