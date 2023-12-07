from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from accounts.models import *
from core.models import *
from django.forms.widgets import Select

USER_CHOICES = [
    ('D', 'Doctor'),
    ('P', 'Patient')
]

#favorite_colors = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=FAVORITE_COLORS_CHOICES,)

#for contact us page
class ContactusForm(forms.ModelForm):
    Name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': "Your Name"}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': "Your E-mail address"}))
    phone_ind = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Your phone country code"}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Your phone number"}))
    message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 5, 'cols': 100, 'placeholder': "Your massage"}))

    
    def __init__(self, *args, **kwargs):                                                        # used to set css classes to the various fields
        super().__init__(*args, **kwargs)
        
    class Meta:
        model = ContactUs
        fields = ('name', 'email','phone_ind','phone_number', 'message')
        
      
class ExpertForm(forms.ModelForm):
    DOB = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    def __init__(self, *args, **kwargs):                                                        # used to set css classes to the various fields
        super().__init__(*args, **kwargs)
        #self.fields['name'].widget.attrs.update({'class': 'textinput form-control'})
        #self.fields['description'].widget.attrs.update({'class': 'textinput form-control'})
        #self.fields['quantity'].widget.attrs.update({'class': 'textinput form-control', 'min': '0'})
        #self.fields['price'].widget.attrs.update({'class': 'textinput form-control', 'min': '0.0'})
     
'''    
class Meta:
        model = Experts
        exclude = ['id','slug', 'status']
        
'''


class EducationModelForm(forms.ModelForm):
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    description= forms.CharField(widget=forms.Textarea(attrs={"rows":2, "cols":20}))
    
    def __init__(self, *args, **kwargs):                                                        # used to set css classes to the various fields
        super().__init__(*args, **kwargs)
        self.fields['institution_name'].widget.attrs.update({'class': 'textinput form-control'})
        #self.fields['description'].widget.attrs.update({'class': 'textinput form-control'})
        #self.fields['quantity'].widget.attrs.update({'class': 'textinput form-control', 'min': '0'})
        #self.fields['price'].widget.attrs.update({'class': 'textinput form-control', 'min': '0.0'})
        
    class Meta:
        model = Education
        exclude = ['id','user', 'slug','email']
        
class Time24hWidget(Select):
    def __init__(self, attrs=None):
        choices = [
            ('00:00', '00:00'),
            ('01:00', '01:00'),
            ('02:00', '02:00'),
            # Add more choices for each hour of the day (00:00 to 23:00)
            # You can generate these choices programmatically if needed.
            # For simplicity, I've only included a few choices here.
            ('23:00', '23:00'),
        ]
        super().__init__(attrs, choices)
             
class TrainingForm(forms.ModelForm):
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    start_time = forms.TimeField(widget=forms.DateInput(attrs={'type': 'time'}))  # Accepts input in 24-hour format)
    end_time = forms.TimeField(widget=forms.DateInput(attrs={'type': 'time'}))
    description= forms.CharField(widget=forms.Textarea(attrs={"rows":2, "cols":20}))
    
    
    class Meta:
        model = Trainings
        exclude = ['id', 'user', 'slug', 'created_on', 'updated_on']
        
class TrainingApplicationForm(forms.ModelForm):
    class Meta:
        model = TrainingApplication
        exclude = ['id', 'slug', 'created_on', 'updated_on']
        widgets = {
        #'password': forms.PasswordInput(),
        #'email': forms.EmailField(required=True)
        
        }