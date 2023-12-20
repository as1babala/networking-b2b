from django.urls import path
from .views import *


app_name = 'product_deals'

urlpatterns = [
   
    path('', ProductDealsListView.as_view(), name='product-deal-list'),
    path('create/', ProductDealCreateView.as_view(), name='product-deal-create'),
    path('<int:pk>/', product_deal_detail, name='product-deal-detail'),
    path('<int:pk>/update/', ProductDealUpdateView.as_view(), name='product-deal-update'),
    path('<int:pk>/delete/', ProductDealDeleteView.as_view(), name='product-deal-delete'),
    path('users/', UserProductDealsListView.as_view(), name='product-deal-user'),
    ### Product Announcement ####
    path('<int:pk>/product_rfi/create/', ProductRFICreateView.as_view(), name='product-rfi-create'),# for review
    path('product_rfi/', ProductRFIListView.as_view(), name='product-rfi-list'),# for review
    path('product_rfi/users/', ProductUserRfiListView.as_view(), name='product-user-rfi-list'),# for review
    path('product_rfi/<int:pk>/', ProductRfiDetailView.as_view(), name='product-rfi-detail'),
    path('search/', ProductDealsSearchView.as_view(), name='product-deal-search'),
    path('product-deal-read-history/', product_deal_read_history, name='product-deal-read-history'), 
    
]