from django.urls import path
from .views import *


app_name = 'projects'

urlpatterns = [
    path('', ProjectListView.as_view(), name='project-list'),
    path('create/', ProjectCreateView.as_view(), name='project-create'),
    path('search/', SearchProjectView.as_view(), name='project-search'),
    #path('<int:id>/generatePDF/', generatePDF, name='generatePDF'),
    
    path('<int:pk>/', ProjectDetailView.as_view(), name='project-detail'), 
    path('<int:pk>/update/', ProjectUpdateView.as_view(), name='project-update'),
    path('<int:pk>/delete/', ProjectDeleteView.as_view(), name='project-delete'),
    path('<int:pk>/document_upload/', ProjectDocumentUpload, name='project-documents'),
    path('reviewed/', ReviewedListView.as_view(), name='project-reviewed'),
    path('approved/', ApprovedListView.as_view(), name='project-approved'),
    path('notreviewed/', NotReviewedListView.as_view(), name='project-notreviewed'),
    path('rejected/', RejectedListView.as_view(), name='project-rejected'),
    #path('pdf/', render_pdf_view, name='project-pdf'),  
]

