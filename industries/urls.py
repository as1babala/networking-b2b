from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import *

app_name = "industries"

urlpatterns = [
    
    path('', IndustryListView.as_view(), name='industry-list'),
    path('create/', IndustryCreateView.as_view(), name='industry-create'),
    #path('<int:pk>/', IndustryDetailView.as_view(), name='industry-detail'),
    #path('<int:pk>/update/', IndustryUpdateView.as_view(), name='industry-update'),
    path('<int:pk>/', IndustryDetailView.as_view(), name='industry-detail'),
    #path('<int:pk>/', detail, name='industry-detail'),
    path('<int:pk>/update/', industry_update, name='industry-update'),
    path('<int:pk>/delete/', IndustryDeleteView.as_view(), name='industry-delete'),
    path('search/', SearchIndView.as_view(), name='industry-search'),
    
    path('sectors/', SectorListView.as_view(), name='sector-list'),
    #path('sectors/', sector_list, name='sector-list'),
    path('sectors/create/', SectorsCreateView.as_view(), name='sector-create'),
    #path('sectors/create/', sector_create, name='sector-create'),
    path('sectors/<int:pk>/', SectorsDetailView.as_view(), name='sector-detail'),
    path('sectors/<int:pk>/update/', SectorsUpdateView.as_view(), name='sector-update'),
    path('sectors/<int:pk>/delete/', SectorsDeleteView.as_view(), name='sector-delete'),
    path('sectors/search/', SearchSectorView.as_view(), name='sector-search'),
    path('import-csv/', import_csv, name='import-csv'),
    #path('success/', success_page, name='success-page'),
    
]