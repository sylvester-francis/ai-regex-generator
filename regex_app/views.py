import os
import re
import json
import regex
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import RegexPattern, RegexRequest, TestCase
from .forms import RegexRequestForm, RegexPatternForm, RegexTestForm, TestCaseForm

def generate_regex_with_ai(description, sample_text, expected_matches):
    """Use OpenAI to generate a regex pattern based on the provided information"""
    try:
        import openai
        client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        
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
        response = client.chat.completions.create(
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
            return {
                "pattern": "Error parsing AI response",
                "explanation": f"The AI did not return valid JSON. Response: {response_text[:100]}...",
                "test_cases": [],
                "flags": ""
            }
            
    except Exception as e:
        return {
            "pattern": "Error generating regex",
            "explanation": f"An error occurred: {str(e)}",
            "test_cases": [],
            "flags": ""
        }

def test_regex(pattern, text, flag_str=""):
    """Test a regex pattern against a text and return match information"""
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
        return {
            "success": False,
            "error": str(e)
        }

def home(request):
    """Home page with regex generator form"""
    form = RegexRequestForm()
    
    # Get recent patterns
    recent_patterns = RegexPattern.objects.order_by('-created_at')[:5]
    
    return render(request, 'regex_app/home.html', {
        'form': form,
        'recent_patterns': recent_patterns
    })

def pattern_list(request):
    """List all saved regex patterns"""
    patterns = RegexPattern.objects.order_by('-created_at')
    return render(request, 'regex_app/pattern_list.html', {
        'patterns': patterns
    })

def pattern_detail(request, pattern_id):
    """View a specific regex pattern with testing functionality"""
    pattern = get_object_or_404(RegexPattern, id=pattern_id)
    test_form = RegexTestForm(initial={
        'regex_pattern': pattern.pattern,
        'test_text': pattern.sample_text
    })
    
    # Get test cases
    test_cases = pattern.test_cases.all()
    
    return render(request, 'regex_app/pattern_detail.html', {
        'pattern': pattern,
        'test_form': test_form,
        'test_cases': test_cases
    })

@csrf_exempt
def generate_regex(request):
    """API endpoint to generate regex with AI"""
    if request.method == 'POST':
        try:
            # Parse the request data
            data = json.loads(request.body)
            description = data.get('description', '')
            sample_text = data.get('sample_text', '')
            expected_matches = data.get('expected_matches', '')
            
            # Create a RegexRequest record
            regex_request = RegexRequest.objects.create(
                description=description,
                sample_text=sample_text,
                expected_matches=expected_matches
            )
            
            # Generate regex with AI
            result = generate_regex_with_ai(description, sample_text, expected_matches)
            
            # Create a RegexPattern
            pattern_name = description[:50] + "..." if len(description) > 50 else description
            regex_pattern = RegexPattern.objects.create(
                name=pattern_name,
                pattern=result['pattern'],
                sample_text=sample_text,
                description=result['explanation']
            )
            
            # Link the pattern to the request
            regex_request.result_pattern = regex_pattern
            regex_request.save()
            
            # Create test cases
            for test_case in result.get('test_cases', []):
                if isinstance(test_case, dict) and 'text' in test_case and 'should_match' in test_case:
                    TestCase.objects.create(
                        regex_pattern=regex_pattern,
                        test_text=test_case['text'],
                        should_match=test_case['should_match']
                    )
            
            # Test the pattern against the sample text
            test_result = test_regex(result['pattern'], sample_text, result.get('flags', ''))
            
            return JsonResponse({
                'status': 'success',
                'pattern': result['pattern'],
                'pattern_id': regex_pattern.id,
                'explanation': result['explanation'],
                'test_result': test_result,
                'flags': result.get('flags', '')
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })
    
    return JsonResponse({
        'status': 'error',
        'message': 'Only POST method is supported'
    })

@csrf_exempt
def test_regex_endpoint(request):
    """API endpoint to test a regex pattern"""
    if request.method == 'POST':
        try:
            # Parse the request data
            data = json.loads(request.body)
            pattern = data.get('pattern', '')
            test_text = data.get('test_text', '')
            flags = data.get('flags', '')
            
            # Test the pattern
            result = test_regex(pattern, test_text, flags)
            
            return JsonResponse({
                'status': 'success',
                'result': result
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })
    
    return JsonResponse({
        'status': 'error',
        'message': 'Only POST method is supported'
    })

def save_pattern(request):
    """Save a new regex pattern"""
    if request.method == 'POST':
        form = RegexPatternForm(request.POST)
        if form.is_valid():
            pattern = form.save()
            messages.success(request, 'Pattern saved successfully!')
            return redirect('pattern_detail', pattern_id=pattern.id)
        else:
            messages.error(request, 'Error saving pattern. Please check the form.')
            
    return redirect('home')

def add_test_case(request, pattern_id):
    """Add a test case to a regex pattern"""
    pattern = get_object_or_404(RegexPattern, id=pattern_id)
    
    if request.method == 'POST':
        form = TestCaseForm(request.POST)
        if form.is_valid():
            test_case = form.save(commit=False)
            test_case.regex_pattern = pattern
            test_case.save()
            messages.success(request, 'Test case added successfully!')
        else:
            messages.error(request, 'Error adding test case. Please check the form.')
            
    return redirect('pattern_detail', pattern_id=pattern.id)