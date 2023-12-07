from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from core.models import *


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('id', 'slug') 