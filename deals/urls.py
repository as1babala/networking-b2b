from django.urls import path
from .views import *


app_name = 'deals'

urlpatterns = [
   
    path('', DealsListView.as_view(), name='deal-list'),
    path('create/', DealCreateView.as_view(), name='deal-create'),
    path('<int:pk>/', deal_detail, name='deal-detail'),
    path('<int:pk>/update/', DealUpdateView.as_view(), name='deal-update'),
    path('<int:pk>/delete/', DealDeleteView.as_view(), name='deal-delete'),
    path('<int:pk>/rfi/', RfiCreateView.as_view(), name='rfi-create'),# for review
    path('search/', DealsSearchView.as_view(), name='deal-search'),
]