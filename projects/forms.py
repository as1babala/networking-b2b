from dataclasses import fields
from email.policy import default
from django import forms
from django.contrib.auth import get_user_model

from django.forms import formset_factory
from core.models import *

class ProjectsForm(forms.ModelForm):
    #reviewed_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    #approved_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    #end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    
    def __init__(self, *args, **kwargs):                                                        # used to set css classes to the various fields
        super().__init__(*args, **kwargs)
    #end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
        
    class Meta:
        model = Projects
        fields = ['company_name','project_name', 'project_description',  'supporting_document']
        
        def clean__FIELD_NAME(self):
            data = self.cleaned_data.get(('FIELD_NAME'))

class ProjectDocumentUploadForm(forms.ModelForm):
    pass


class ProjectReviewedForm(forms.ModelForm):
    class Meta:
        #model=Projects
        #fields = ['reviewed','reviewed_by', 'reviewer_observations']
        pass
class ProjectApprovedForm(forms.ModelForm):
    class Meta:
        pass
       #model=Projects
        #fields = ['approved','approved_by', 'approver_observations']