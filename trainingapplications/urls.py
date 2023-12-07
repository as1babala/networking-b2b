from django.urls import path
from .views import *


app_name = 'trainingapplications'

urlpatterns = [
   
    path('', TrainingApplicationListView.as_view(), name='training-app-list'),
    path('<int:pk>/', TrainingApplicationDetailView.as_view(), name='training-app-detail'),
    path('<int:pk>/update/', TrainingApplicationUpdateView.as_view(), name='training-app-update'),
    path('user/', UserTrainingApplicationListView.as_view(), name='user-training-app-list'),
    
    
]