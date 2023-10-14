from django.urls import path
from .views import *


app_name = 'trainings'

urlpatterns = [
   
    path('', TrainingListView.as_view(), name='training-list'),
    path('create/', TrainingCreateView.as_view(), name='training-create'),
    path('<int:pk>/', TrainingDetailView.as_view(), name='training-detail'),
    path('<int:pk>/update/', TrainingUpdateView.as_view(), name='training-update'),
    path('<int:pk>/member/applications/', MemberApplicationCreateView.as_view(), name='application-create'),# for review
    path('<int:pk>/non_member/applications/', NewApplicationCreateView.as_view(), name='non-member-create'),# for review
    path('<int:pk>/delete/', TrainingDeleteView.as_view(), name='training-delete'),
    path('search/', TrainingSearchView.as_view(), name='training-search'),
    
]