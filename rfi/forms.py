from dataclasses import fields
from email.policy import default
from django import forms
from django.contrib.auth import get_user_model
from django.forms import formset_factory, inlineformset_factory, modelform_factory, modelformset_factory
from employees.models import *
from accounts.models import *
from core.models import *
from tinymce.widgets import TinyMCE

class RfiForm(forms.ModelForm):
    message = forms.CharField(widget=TinyMCE(), label="send a request to the owner of this advertisement")
    class Meta:
        model = Rfi
        fields = [ 'message']
    
        widgets = {
            'name': forms.TextInput(attrs={'readonly': True}),
            'email': forms.EmailInput(attrs={'readonly': True}),
            #'phone': forms.TextInput(attrs={'readonly': True}),
            'message': forms.TextInput(attrs={'placeholder': 'Leave a request for information'}),
        }