from dataclasses import fields
from email.policy import default
from django import forms
from django.contrib.auth import get_user_model
from core.models import *


class CSVImportForm(forms.Form):
    csv_file = forms.FileField()
    
    
class IndustryForm(forms.ModelForm):
        
    class Meta:
        model = Industry
        fields = (
            'name',
            'description',
            
        )
        
        
class SectorsForm(forms.ModelForm):
    class Meta:
        model = Sectors
        fields = (
            'industry',
            'name',
            'description'
        )
        widgets = {
            'Industry': forms.TextInput(attrs={'readonly': True}),
            'name': forms.TextInput(attrs={'readonly': False}),
            'description': forms.Textarea(attrs={'placeholder': 'Place the sector description'})
        }
     