from dataclasses import fields
from email.policy import default
from django import forms
from django.contrib.auth import get_user_model
from django.forms import formset_factory
from dynamic_forms import DynamicField, DynamicFormMixin
from core.models import *
from common.utils import *
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import admin
from django_cascading_dropdown_widget.widgets import DjangoCascadingDropdownWidget
from django_cascading_dropdown_widget.widgets import CascadingModelchoices


ACTIVE = (('YES', 'YES'), ('NO','NO'))
class EnterprisesForm(DynamicFormMixin, forms.ModelForm):
    registration_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Enterprises
        exclude = ['created_on', 'updated_on', 'active', 'slug', 'user','company_id', 'id']
        
    def __init__(self, *args, **kwargs):                                                        # used to set css classes to the various fields
        super().__init__(*args, **kwargs)
        self.fields['sector'].queryset = Sectors.objects.none()

        if 'industry' in self.data:
            try:
                industry_id = int(self.data.get('industry'))
                self.fields['sector'].queryset = Sectors.objects.filter(industry_id=industry_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['sector'].queryset = self.instance.industry.sector_set.order_by('name')


        #self.fields['sector'].queryset = self.instance.industry.sector_set.order_by('name')
        self.fields['first_name'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Enter your first name'})
        self.fields['last_name'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Enter your last name'})
        self.fields['email'].widget.attrs.update({'class': 'email form-control', 'placeholder':'Enter your email address'})
        self.fields['phone_code'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Enter your country code'})
        self.fields['registration_id'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Enter the company registration ID'}) 
        self.fields['phone_number'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Enter your phone number'})
        self.fields['company_name'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Enter your company name'}) 
        self.fields['company_type'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Enter your company type'}) 
        self.fields['company_email'].widget.attrs.update({'class': 'email form-control', 'placeholder':'Enter your company email address'}) 
        self.fields['company_web'].widget.attrs.update({'class': 'web address form-control', 'placeholder':'Enter your company website address'}) 
        self.fields['company_address'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Enter your company physical address'}) 
        self.fields['company_country'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Enter your company country'})
        self.fields['company_city'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Enter your company city'}) 
        self.fields['industry'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Enter your company industry'}) 
        self.fields['sector'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Enter your company sector of activities'})
        self.fields['number_employees'].widget.attrs.update({'class': 'textinput form-control', 'placeholder':'Number of employees'})
        commercial = forms.CharField(widget = forms.CheckboxInput)
        technical = forms.CharField(widget = forms.CheckboxInput)
        financial = forms.CharField(widget = forms.CheckboxInput)
        management = forms.CharField(widget = forms.CheckboxInput)
        activity_description = forms.CharField(widget=forms.Textarea(attrs={"rows":3, "cols":30}))
        registration_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
        #self.fields['registration_date'].widget.attrs.update({'class': 'date form-control', 'placeholder':'Number of employees'})
        
        

    
        