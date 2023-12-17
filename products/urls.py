from django.urls import path
from .views import *


app_name = 'products'

urlpatterns = [
   
    #path('', product_home, name='stripe-list'),
    #path('checkout/', CreateCheckoutSessionView.as_view, name='create-checkout-session'),
    path('checkout/', create_checkout_session, name='create-checkout-session'),
    path('', ProductLandingPageView.as_view(), name='landing-page'),
    path('create/', ProductCreateView.as_view(), name='product-create'),
    path('products/', ProductListView.as_view(), name='product-list'),
    
]