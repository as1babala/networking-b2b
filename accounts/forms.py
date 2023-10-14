from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *
#from employees.models import *

USER_CHOICES = [
    ('EXPERT', 'EXPERT'),
    ('COMPANY', 'COMPANY')
]

PARTNERSHIP_TYPE = (('COMMERCIAL', 'COMMERCIAL'),('TECHNIQUE', 'TECHNIQUE'),('FINANCIER', 'FINANCIER'), ('MANAGEMENT', 'MANAGEMENT'))
class UserCreateForm(UserCreationForm):
    #user_type = forms.ChoiceField(choices=USER_CHOICES, required=True, widget=forms.RadioSelect)
    #first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': "Your first name"}))
    #last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': "Your last name"}))
    #username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': "Your username"}))
    #email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': "Your E-mail address"}))
    #password = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={'placeholder': "Your password"}))
    #partnership_type = forms.MultipleChoiceField(choices=PARTNERSHIP_TYPE,widget=forms.CheckboxSelectMultiple)
    #partnership_type = forms.MultipleChoiceField(choices=PARTNERSHIP_TYPE)
    
    class Meta:
        model = CustomUser
        fields = [
           
            'first_name','last_name', 'username', 'email', 'is_company', 'is_expert' ,'company_name',
            'commercial', 'technical', 'financial', 'management'
            ]
        widgets = {
        'password': forms.PasswordInput()
        }
        
#for contact us page
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': "Your Name"}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': "Your E-mail address"}))
    phone_ind = forms.CharField(max_length=3, widget=forms.TextInput(attrs={'placeholder': "Your phone country code"}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Your phone number"}))
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30, 'placeholder': "Your massage"}))

    class Meta:
        model = ContactUs
        fields = ('email','phone_ind','phone_number','message')