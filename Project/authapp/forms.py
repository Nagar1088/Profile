from django import forms
from .models import ContactRequest, Project, Skill
from django.core.validators import EmailValidator
from django.utils.html import strip_tags

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactRequest
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your@email.com'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Your message...'
            }),
        }

    def clean_message(self):
        message = self.cleaned_data.get('message')
        stripped_message = strip_tags(message)
        if len(stripped_message) < 10:
            raise forms.ValidationError("Message must be at least 10 characters long.")
        return stripped_message

class ProjectForm(forms.ModelForm):
    technologies = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Comma-separated technologies'
        }),
        help_text="Separate technologies with commas"
    )

    class Meta:
        model = Project
        fields = [
            'title', 'slug', 'description', 'image',
            'github_url', 'live_url', 'technologies',
            'category', 'featured'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_technologies(self):
        technologies = self.cleaned_data.get('technologies')
        return ', '.join([t.strip() for t in technologies.split(',')])

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'proficiency', 'category', 'order', 'show_in_chart']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'proficiency': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 100
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'show_in_chart': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }