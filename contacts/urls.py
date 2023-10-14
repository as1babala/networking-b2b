from django.urls import path
from .views import *


app_name = 'contacts'

urlpatterns = [
    path('', ContactListView.as_view(), name='contact-list'),
    path('create/', ContactCreateView.as_view(), name='contact-create'),
    path('<int:pk>/', ContactDetailView.as_view(), name='contact-detail'),
    path('search/', SearchContactView.as_view(), name='contact-search'),
    
]