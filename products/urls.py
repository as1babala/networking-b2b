from django.urls import path
from .views import *


app_name = 'products'

urlpatterns = [
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('create-checkout-session/<int:pk>/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
     path('subscribe/<int:product_id>/', create_subscription, name='create-subscription'),
    path('create/', ProductCreateView.as_view(), name='product-create'),
    path('', ProductListView.as_view(), name='product-list'),
    path('payment_success/', SuccessView.as_view(), name='payment-success'),
    path('payment_cancel/', CancelView.as_view(), name='payment-cancel'),
     path('payments/webhook/', stripe_webhook, name='stripe-webhook'),
     
    path('<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('list/', ServicesView.as_view(), name='services'),
    
]

    