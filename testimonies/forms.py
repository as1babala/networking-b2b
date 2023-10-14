from dataclasses import fields
from email.policy import default
from django import forms
from django.contrib.auth import get_user_model
from django.forms import formset_factory, inlineformset_factory, modelform_factory, modelformset_factory
from employees.models import *
from accounts.models import *
from core.models import *

class TestimonyForm(forms.ModelForm):
    class Meta:
        model = Testimonies
        exclude = ('id', 'slug', 'user')