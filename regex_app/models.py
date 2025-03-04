from django.db import models

class RegexPattern(models.Model):
    name = models.CharField(max_length=100, help_text="Name or description of the regex pattern")
    pattern = models.TextField(help_text="The regex pattern string")
    sample_text = models.TextField(help_text="Sample text that the regex should match", blank=True)
    description = models.TextField(help_text="Description or explanation of what the regex does", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class RegexRequest(models.Model):
    description = models.TextField(help_text="Description of what you want the regex to do")
    sample_text = models.TextField(help_text="Sample text to match or validate")
    expected_matches = models.TextField(help_text="What parts of the sample text should be matched", blank=True)
    result_pattern = models.ForeignKey(RegexPattern, null=True, blank=True, on_delete=models.SET_NULL, related_name="requests")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Request: {self.description[:50]}"

class TestCase(models.Model):
    regex_pattern = models.ForeignKey(RegexPattern, on_delete=models.CASCADE, related_name="test_cases")
    test_text = models.TextField(help_text="Text to test against the regex pattern")
    should_match = models.BooleanField(default=True, help_text="Whether the test text should match the pattern")
    
    def __str__(self):
        return f"Test for {self.regex_pattern.name}: {'Should match' if self.should_match else 'Should not match'}"