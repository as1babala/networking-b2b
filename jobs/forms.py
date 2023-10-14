from dataclasses import fields
from email.policy import default
from django import forms
from django.contrib.auth import get_user_model
from .models import *
from django.forms import formset_factory
from core.models import *



class JobForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    #end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Jobs
        exclude = ['created_on', 'updated_on','slug','id','company_name', 'job_contact', 'email']




class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        exclude = ['created_on', 'updated_on','slug','id']