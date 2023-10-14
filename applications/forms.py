from dataclasses import fields
from email.policy import default
from django import forms
from django.contrib.auth import get_user_model
from .models import *
from django.forms import formset_factory
from core.models import *




class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        exclude = [ 'id','job','user','email']