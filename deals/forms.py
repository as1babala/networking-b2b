from dataclasses import fields
from email.policy import default
from django import forms
from django.contrib.auth import get_user_model
from .models import *
from django.forms import ClearableFileInput
from django.forms import formset_factory
from employees.models import *
from core.models import *



class DealsForm(forms.ModelForm):
    class Meta:
        model = Deals
        exclude = [ 'id','slug', 'dealer', 'email', 'company_name']
        
        def clean__FIELD_NAME(self):
            data = self.cleaned_data.get(('FIELD_NAME'))
            
class DealImagesForm(forms.Form):
    image = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    
    model = DealImages
    fields = ('image',)
    
    