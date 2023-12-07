from dataclasses import fields
from email.policy import default
from django import forms
from django.contrib.auth import get_user_model

from django.forms import formset_factory
from core.models import *
from ckeditor.widgets import CKEditorWidget
class ProjectsForm(forms.ModelForm):
    #project_description = forms.CharField(widget=CKEditorWidget())
    
    #reviewed_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    #approved_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    #end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    
    def __init__(self, *args, **kwargs):                                                        # used to set css classes to the various fields
        super().__init__(*args, **kwargs)
    #end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
        
    class Meta:
        model = Projects
        fields = ['company_name','project_name', 'project_category', 'project_description',  'estimated_cost', 'estimated_Annual_revenue',
              'supporting_document',
              
          ]
        
        def clean__FIELD_NAME(self):
            data = self.cleaned_data.get(('FIELD_NAME'))

class ProjectReviewedForm(forms.ModelForm):
    class Meta:
        model=Projects
        fields = ['reviewed', 'reviewer_observations']
        widgets = {
            'reviewed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
class ProjectApprovedForm(forms.ModelForm):
    final_decision = forms.ChoiceField(widget=forms.RadioSelect, choices=PROJECT_DECISION)
    class Meta:
        model=Projects
        fields = ['approved','final_decision', 'approver_observations']
        widgets = {
            'approved': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
#creating a multiple level create view
        

