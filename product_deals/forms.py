from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from accounts.models import *
from core.models import *
from django.forms.widgets import Select



class ProductDealsForm(forms.ModelForm):
    availability_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    #expiration_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = ProductDeals
        exclude = ['created_on', 'updated_on','slug','id', 'email', 'dealer', 'company_name']
        
        def clean__FIELD_NAME(self):
            data = self.cleaned_data.get(('FIELD_NAME'))

class ProductDealImagesForm(forms.Form):
    image = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    
    model = ProductDealImages
    fields = ('image',)           
class ProductRFIForm(forms.ModelForm):
    class Meta:
        model = ProductRFI
        exclude = ['created_on', 'updated_on','slug','id', 'client_email', 'client_name', 'product_deal']
        
        def clean__FIELD_NAME(self):
            data = self.cleaned_data.get(('FIELD_NAME'))