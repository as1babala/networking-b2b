from django.urls import path
from .views import *


app_name = 'jobs'

urlpatterns = [
   
    path('', JobListView.as_view(), name='job-list'),
    path('create/', JobCreateView.as_view(), name='job-create'),
    path('<int:pk>/', JobDetailView.as_view(), name='job-detail'),
    path('<int:pk>/update/', JobUpdateView.as_view(), name='job-update'),
    path('<int:pk>/delete/', JobDeleteView.as_view(), name='job-delete'),
    path('search/', JobSearchView.as_view(), name='job-search'),
    path('<int:pk>/applications/', ApplicationCreateView.as_view(), name='application-create'),# for review
    #path('<int:pk>/applications/', apply_job, name='application-create'),# for review
    #path('<int:pk>/applications/', apply_for_job, name='application-create'),# for review
    path('application/<int:pk>/resume_upload/', ApplicationResumeUploadView.as_view(), name='application-resume-upload'),
    ######
    #path('<slug:slug>/', JobDetailView.as_view(), name='job-detail'),
    #path('<slug:slug>/update/', JobUpdateView.as_view(), name='job-update'),
    #path('<slug:slug>/delete/', JobDeleteView.as_view(), name='job-delete'),
    #path('<slug:slug>/applications/', ApplicationCreateView.as_view(), name='application-create'),# for review
]