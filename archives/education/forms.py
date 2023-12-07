from dataclasses import fields
from email.policy import default
from django import forms
from django.contrib.auth import get_user_model
from django.forms import formset_factory, inlineformset_factory, modelform_factory, modelformset_factory
from core.models import *
from accounts.models import *


class EducationModelForm(forms.ModelForm):
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    description= forms.CharField(widget=forms.Textarea(attrs={"rows":3, "cols":20}))
    
    def __init__(self, *args, **kwargs):                                                        # used to set css classes to the various fields
        super().__init__(*args, **kwargs)
        self.fields['institution_name'].widget.attrs.update({'class': 'textinput form-control'})
        #self.fields['description'].widget.attrs.update({'class': 'textinput form-control'})
        #self.fields['quantity'].widget.attrs.update({'class': 'textinput form-control', 'min': '0'})
        #self.fields['price'].widget.attrs.update({'class': 'textinput form-control', 'min': '0.0'})
        
    class Meta:
        model = Education
        exclude = ['id','user', 'slug','email']
