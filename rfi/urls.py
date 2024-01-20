from django.urls import path
from .views import *


app_name = 'rfi'

urlpatterns = [
    path('', RfiListView.as_view(), name='rfi-list'),
    path('user/', UserRfiListView.as_view(), name='rfi-user'),
    #path('create/', RfiCreateView.as_view(), name='rfi-create'),
    path('<slug:slug>/', RfiDetailView.as_view(), name='rfi-detail'),
    path('<slug:slug>/update/', RfiUpdateView.as_view(), name='rfi-update'),
    path('<slug:slug>/delete/', RfiDeleteView.as_view(), name='rfi-delete'),
    
]