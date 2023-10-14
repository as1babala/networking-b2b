from email.policy import default
from django import forms
from django.contrib.auth import get_user_model
from django.forms import formset_factory, inlineformset_factory, modelform_factory, modelformset_factory
from core.models import *



class FicheTechnicForm(forms.ModelForm):
    
    class Meta:
        model = FicheTechnic
        exclude = ['id','slug','fiche_id']