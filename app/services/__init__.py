"""
Services initialization module
"""
from app.services.ai_service import generate_regex_with_ai
from app.services.regex_service import test_regex, get_flag_descriptions, explain_regex_component
from app.services.db_service import (
    create_pattern,
    get_pattern,
    get_patterns,
    update_pattern,
    delete_pattern,
    create_test_case,
    get_test_cases,
    delete_test_case,
    create_request
)

__all__ = [
    'generate_regex_with_ai',
    'test_regex',
    'get_flag_descriptions',
    'explain_regex_component',
    'create_pattern',
    'get_pattern',
    'get_patterns',
    'update_pattern',
    'delete_pattern',
    'create_test_case',
    'get_test_cases',
    'delete_test_case',
    'create_request'
]