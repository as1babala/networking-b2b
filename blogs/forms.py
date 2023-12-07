from dataclasses import fields
from email.policy import default
from django import forms
from tinymce.widgets import TinyMCE
from django.contrib.auth import get_user_model
from django.forms import formset_factory, inlineformset_factory, modelform_factory, modelformset_factory

from accounts.models import *
from core.models import *

class BlogForm(forms.ModelForm):
    #content = forms.CharField(widget=TinyMCE(), label="Please leave a review for this blog")
    
    class Meta:
        model = Blog
        exclude = ('id', 'slug', 'author', 'email')


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ('id', 'slug', 'reviewer',  'blog', 'created_on')


class ReplyToReviewForm(forms.ModelForm):
    class Meta:
        model = ReplyToReview
        exclude= ('id', 'slug', 'replier',  'review', 'created_on')
        
        
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ('id',)