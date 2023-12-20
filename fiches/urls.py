from django.urls import path
from .views import *


app_name = 'fiches'

urlpatterns = [
    path('', FicheTechnicListView.as_view(), name='fiche-list'),
    path('create/', FicheTechnicCreateView.as_view(), name='fiche-create'),
    #path('<int:pk>/', FicheTechnicDetailView.as_view(), name='fiche-detail'),
    #path('<slug>/', FicheTechnicDetailView.as_view(), name='fiche-detail'),
    path('<int:pk>/update/', FicheTechnicUpdateView.as_view(), name='fiche-update'),
    #path('<slug>/update/', FicheTechnicUpdateView.as_view(), name='fiche-update'),
    path('<int:pk>/delete/', FicheTechnicDeleteView.as_view(), name='fiche-delete'),
    path('search/', FicheTechnicSearchView.as_view(), name='fiche-search'),
    path('fiche-read-history/', fiche_read_history, name='fiche-read-history'),
    path('<slug>/', fiche_detail, name='fiche-detail'), 
    
    
]