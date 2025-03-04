from django import forms
from .models import RegexPattern, RegexRequest, TestCase

class RegexRequestForm(forms.ModelForm):
    class Meta:
        model = RegexRequest
        fields = ['description', 'sample_text', 'expected_matches']
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'E.g., "I need a regex to extract email addresses from text"'
            }),
            'sample_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Enter sample text containing examples you want to match'
            }),
            'expected_matches': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter specific parts of the sample text that should be matched (one per line)'
            }),
        }

class RegexPatternForm(forms.ModelForm):
    class Meta:
        model = RegexPattern
        fields = ['name', 'pattern', 'sample_text', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'E.g., "Email Extractor"'
            }),
            'pattern': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter regex pattern'
            }),
            'sample_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter sample text to test the pattern'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter a description of what this regex does'
            }),
        }

class RegexTestForm(forms.Form):
    regex_pattern = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter a regex pattern to test'
        })
    )
    test_text = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Enter text to test against the pattern'
        })
    )
    flags = forms.MultipleChoiceField(
        required=False,
        choices=[
            ('i', 'Case insensitive (i)'),
            ('m', 'Multi-line (m)'),
            ('s', 'Dot matches newline (s)'),
            ('x', 'Verbose (x)'),
        ],
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        })
    )

class TestCaseForm(forms.ModelForm):
    class Meta:
        model = TestCase
        fields = ['test_text', 'should_match']
        widgets = {
            'test_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter test text'
            }),
            'should_match': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }