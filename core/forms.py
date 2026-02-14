from django import forms
from .models import ContactInquiry


class ContactForm(forms.ModelForm):
    """General contact form."""

    class Meta:
        model = ContactInquiry
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your Name',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'your@email.com',
                'required': True,
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Your message...',
                'rows': 5,
                'required': True,
            }),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.inquiry_type = 'general'
        if commit:
            instance.save()
        return instance


class ProjectInquiryForm(forms.ModelForm):
    """Project inquiry form with additional fields."""

    class Meta:
        model = ContactInquiry
        fields = ['name', 'email', 'project_description', 'budget', 'timeline', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your Name',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'your@email.com',
                'required': True,
            }),
            'project_description': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Describe your project idea...',
                'rows': 4,
                'required': True,
            }),
            'budget': forms.Select(attrs={
                'class': 'form-input',
            }),
            'timeline': forms.Select(attrs={
                'class': 'form-input',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Any additional details or questions...',
                'rows': 3,
            }),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.inquiry_type = 'project'
        if commit:
            instance.save()
        return instance
