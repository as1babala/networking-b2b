from dataclasses import fields
from email.policy import default
from django import forms
from django.contrib.auth import get_user_model
from .models import *
from django.forms import formset_factory
from employees.models import *
from core.models import *



class DealsForm(forms.ModelForm):
    class Meta:
        model = Deals
        fields = [ 'deal_title','category','deal_type', 'descriptions','deal_picture']
        
        def clean__FIELD_NAME(self):
            data = self.cleaned_data.get(('FIELD_NAME'))