from django.urls import path
from .views import *


app_name = 'analytics'

urlpatterns = [
    #path('', main_analytics, name='blog-stats'),
    path('', MainAnalyticsView.as_view(), name='analytics'),
]
    