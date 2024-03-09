from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from core.models import *
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
    email = forms.EmailField(max_length=200, label="Email Address", required=True, help_text='Required') 
    class Meta:
        model = CustomUser
       
        widgets = {
        'password': forms.PasswordInput(),
     
       
        
        #'email': forms.EmailField()
        
        }
        fields = [
           
            'salutations','first_name','last_name', 'username', 'email' ,'company_name',
            'commercial', 'technical', 'financial', 'management', 'password1', 'password2','agreement'
            ]

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
        
class WorkExperienceForm(forms.ModelForm):
    #start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    #end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = WorkExperience
        exclude = ('id', 'user', 'created_on', 'email')

    widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
           
        }        

class ProjectPortfolioForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = ExpertPortfolio
        exclude = ('id', 'consultant', 'created_on', 'consultant_email')
        
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
           
        }
        
class EducationModelForm(forms.ModelForm):
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    description= forms.CharField(widget=forms.Textarea(attrs={"rows":3, "cols":20}))
    
    def __init__(self, *args, **kwargs):                                                        # used to set css classes to the various fields
        super().__init__(*args, **kwargs)
        self.fields['institution_name'].widget.attrs.update({'class': 'textinput form-control'})
    widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.TimeInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'cols': 3, 'rows': 1}),
        }
    class Meta:
        model = Education
        exclude = ['id','user', 'slug']

