from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from core.models import *



class ExpertProfileForm(forms.Form):
    #user_type = forms.ChoiceField(choices=USER_CHOICES, required=True, widget=forms.RadioSelect)
    #first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': "Your first name"}))
    #last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': "Your last name"}))
    #username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': "Your username"}))
    #email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': "Your E-mail address"}))
    #password = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={'placeholder': "Your password"}))
    #partnership_type = forms.MultipleChoiceField(choices=PARTNERSHIP_TYPE,widget=forms.CheckboxSelectMultiple)
    #partnership_type = forms.MultipleChoiceField(choices=PARTNERSHIP_TYPE)
    class Meta:
        model = ExpertProfile
        exclude = ['created_on', 'updated_on', 'active', 'slug', 'user','is_expert', 'id']

class CompanyProfileForm(forms.Form):
    #user_type = forms.ChoiceField(choices=USER_CHOICES, required=True, widget=forms.RadioSelect)
    #first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': "Your first name"}))
    #last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': "Your last name"}))
    #username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': "Your username"}))
    #email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': "Your E-mail address"}))
    #password = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={'placeholder': "Your password"}))
    #partnership_type = forms.MultipleChoiceField(choices=PARTNERSHIP_TYPE,widget=forms.CheckboxSelectMultiple)
    #partnership_type = forms.MultipleChoiceField(choices=PARTNERSHIP_TYPE)
    class Meta:
        model = CompanyProfile
        exclude = ['created_on', 'updated_on', 'active', 'slug', 'user','is_company', 'id', 'company_name']



class EmployeeProfileForm(forms.Form):
    #user_type = forms.ChoiceField(choices=USER_CHOICES, required=True, widget=forms.RadioSelect)
    #first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': "Your first name"}))
    #last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': "Your last name"}))
    #username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': "Your username"}))
    #email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': "Your E-mail address"}))
    #password = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={'placeholder': "Your password"}))
    #partnership_type = forms.MultipleChoiceField(choices=PARTNERSHIP_TYPE,widget=forms.CheckboxSelectMultiple)
    #partnership_type = forms.MultipleChoiceField(choices=PARTNERSHIP_TYPE)
    class Meta:
        model = EmployeeProfile
        exclude = ['created_on', 'updated_on', 'active', 'slug', 'user','is_employee', 'id', ]
        

class AdminProfileForm(forms.Form):
    #user_type = forms.ChoiceField(choices=USER_CHOICES, required=True, widget=forms.RadioSelect)
    #first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': "Your first name"}))
    #last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': "Your last name"}))
    #username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': "Your username"}))
    #email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': "Your E-mail address"}))
    #password = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={'placeholder': "Your password"}))
    #partnership_type = forms.MultipleChoiceField(choices=PARTNERSHIP_TYPE,widget=forms.CheckboxSelectMultiple)
    #partnership_type = forms.MultipleChoiceField(choices=PARTNERSHIP_TYPE)
    class Meta:
        model = AdminProfile
        exclude = ['created_on', 'updated_on', 'active', 'slug', 'user','is_employee', 'id', ]  