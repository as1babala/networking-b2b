from django.urls import path
from .views import *


app_name = 'experts'

urlpatterns = [
    path('', ExpertsListView.as_view(), name='expert-list'),
    path('create/', ExpertsCreateView.as_view(), name='expert-create'),
    path('<int:pk>/', expert_detail, name='expert-detail'),
    #path('<slug:slug>/', ExpertsDetailView.as_view(), name='expert-detail'),
    path('<int:pk>/update/', ExpertsUpdateView.as_view(), name='expert-update'),
    path('<int:pk>/delete/', ExpertsDeleteView.as_view(), name='expert-delete'),
    path('search/', SearchResultsView.as_view(), name='expert-search'),
    
   
    
]