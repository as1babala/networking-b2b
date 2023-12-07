from django.urls import path
from .views import *


app_name = 'education'

urlpatterns = [
    path('', EducationListView.as_view(), name='education-list'),
    path('my_education/', UserEducationListView, name='education-user'),
    path('create/', EducationCreateView.as_view(), name='education-create'),
    path('<int:pk>/', EducationDetailView.as_view(), name='education-detail'),
    path('search/', EducationSearchView.as_view(), name='education-search'),
    #path('<int:pk>/update/', EducationUpdateView.as_view(), name='education-update'),
    #path('<int:pk>/delete/', EducationDeleteView.as_view(), name='education-delete'),
    
]