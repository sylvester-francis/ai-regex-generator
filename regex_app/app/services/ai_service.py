"""
Service for AI-powered regex generation
"""
import os
import json
import logging
from typing import Dict, Any, Optional

# Initialize logger
logger = logging.getLogger(__name__)

async def generate_regex_with_ai(
    description: str, 
    sample_text: str, 
    expected_matches: Optional[str] = None
) -> Dict[str, Any]:
    """
    Use OpenAI to generate a regex pattern based on the provided information
    
    Args:
        description: Description of what the regex should do
        sample_text: Sample text containing examples of what to match
        expected_matches: Specific parts of the sample text that should match
        
    Returns:
        Dictionary containing pattern, explanation, test cases, and flags
    """
    try:
        import openai
        
        # Get API key from environment variable
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            logger.error("OPENAI_API_KEY not found in environment variables")
            return {
                "pattern": "Error: API key not found",
                "explanation": "Please set the OPENAI_API_KEY environment variable",
                "test_cases": [],
                "flags": ""
            }
            
        client = openai.OpenAI(api_key=api_key)
        
        # Prepare the prompt
        prompt = f"""Generate a regular expression for the following requirement:
Description: {description}

Sample text:
```
{sample_text}
```

"""

        if expected_matches:
            prompt += f"""Expected matches:
```
{expected_matches}
```

"""

        prompt += """Respond ONLY with a JSON object that has the following fields:
1. "pattern": the regex pattern string
2. "explanation": a step-by-step explanation of how the regex works
3. "test_cases": an array of sample texts that should or shouldn't match (at least 3 examples)
4. "flags": any regex flags that should be used (i, m, s, etc.)

Return ONLY the JSON and nothing else."""

        # Call OpenAI API
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You're a regex expert. Create precise regex patterns that match exactly what's needed, no more and no less."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        
        # Parse the response
        response_text = response.choices[0].message.content
        logger.debug(f"AI response: {response_text}")
        
        # Extract JSON from the response
        try:
            # Check if the response starts with ```json and ends with ```
            if response_text.startswith("```json") and "```" in response_text.split("```json", 1)[1]:
                json_str = response_text.split("```json", 1)[1].split("```", 1)[0].strip()
                result = json.loads(json_str)
            else:
                # Try to parse the whole response as JSON
                result = json.loads(response_text)
                
            return result
            
        except json.JSONDecodeError:
            logger.error(f"Failed to parse AI response as JSON: {response_text}")
            return {
                "pattern": "Error parsing AI response",
                "explanation": f"The AI did not return valid JSON. Response: {response_text[:100]}...",
                "test_cases": [],
                "flags": ""
            }
            
    except Exception as e:
        logger.exception("Error generating regex with AI")
        return {
            "pattern": "Error generating regex",
            "explanation": f"An error occurred: {str(e)}",
            "test_cases": [],
            "flags": ""
        }