from django.urls import path
from .views import  *


app_name = 'applications'

urlpatterns = [
   
        path('', ApplicationsListView.as_view(), name='application-list'),
        path('user/', ApplicationsListView2.as_view(), name='application-user'),
        path('<int:pk>/delete/', ApplicationDeleteView.as_view(), name='application-delete'),
        #path('create/', JobApplicationCreateView.as_view(), name='application-create') 
        #path('<int:pk>/update/', FicheTechnicUpdateView.as_view(), name='fiche-update'),
        #path('<slug>/update/', FicheTechnicUpdateView.as_view(), name='fiche-update'),
        path('<int:pk>/update/', ApplicationUpdateView.as_view(), name='application-update'),
        path('<int:pk>/', ApplicationDetailView.as_view(), name='application-detail'),
        #path('<int:pk>/update/', application_update, name='application-update')    
    
]
