from django.urls import path
from .views import *


app_name = 'testimonies'

urlpatterns = [
     path('', TestimonyListView.as_view(), name='testimony-list'),
    path('create/', TestimonyCreateView.as_view(), name='testimony-create'),
    path('<int:pk>/', TestimonyDetailView.as_view(), name='testimony-detail'),
     path('search/', TestimonySearchView.as_view(), name='testimony-search'),
    
    
]