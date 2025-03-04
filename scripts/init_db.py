"""
Script to initialize the database with sample data
"""
import asyncio
import sys
import os

# Add parent directory to path so we can import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import create_db_and_tables, async_session
from app.models import RegexPattern, TestCase


async def create_sample_data():
    """Create sample regex patterns and test cases"""
    async with async_session() as db:
        # Sample patterns
        patterns = [
            {
                "name": "Email Extractor",
                "pattern": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
                "sample_text": "Contact us at info@example.com or support@company.co.uk.",
                "description": "Extracts email addresses from text. Matches the username, @ symbol, domain name, and top-level domain.",
                "test_cases": [
                    {"test_text": "info@example.com", "should_match": True},
                    {"test_text": "user.name+tag@domain.co.uk", "should_match": True},
                    {"test_text": "invalid@email", "should_match": False},
                ]
            },
            {
                "name": "URL Validator",
                "pattern": r"https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)",
                "sample_text": "Visit our website at https://example.com or http://www.company.co/products.",
                "description": "Validates URLs with http or https protocols. Includes optional www prefix and path components.",
                "test_cases": [
                    {"test_text": "https://example.com", "should_match": True},
                    {"test_text": "http://www.example.com/path?query=value", "should_match": True},
                    {"test_text": "ftp://example.com", "should_match": False},
                ]
            },
            {
                "name": "Date Extractor (YYYY-MM-DD)",
                "pattern": r"\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12][0-9]|3[01])",
                "sample_text": "The meeting is scheduled for 2023-05-15 and the deadline is 2023-06-30.",
                "description": "Extracts dates in the YYYY-MM-DD format. Validates that month is between 01-12 and day is between 01-31.",
                "test_cases": [
                    {"test_text": "2023-05-15", "should_match": True},
                    {"test_text": "2023-13-01", "should_match": False},
                    {"test_text": "2023-05-32", "should_match": False},
                ]
            },
        ]
        
        # Create patterns and test cases
        for pattern_data in patterns:
            # Create pattern
            test_cases_data = pattern_data.pop("test_cases")
            pattern = RegexPattern(**pattern_data)
            db.add(pattern)
            await db.flush()  # Flush to get the ID
            
            # Create test cases
            for test_case_data in test_cases_data:
                test_case = TestCase(
                    regex_pattern_id=pattern.id,
                    **test_case_data
                )
                db.add(test_case)
        
        # Commit all changes
        await db.commit()
        print(f"Created {len(patterns)} sample patterns with test cases")


async def main():
    """Main function to initialize the database"""
    print("Initializing database...")
    
    # Create tables
    await create_db_and_tables()
    print("Tables created successfully")
    
    # Create sample data
    await create_sample_data()
    print("Database initialized successfully")


if __name__ == "__main__":
    asyncio.run(main())