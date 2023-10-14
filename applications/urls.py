from django.urls import path
from .views import *


app_name = 'applications'

urlpatterns = [
   
    path('', ApplicationsListView.as_view(), name='application-list'),
    path('my_applications/', UserApplicationsListView, name='application-user')
    #path('create/', JobApplicationCreateView.as_view(), name='application-create'),
    
]
