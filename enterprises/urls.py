from django.urls import path
from .views import *


app_name = 'enterprises'

urlpatterns = [
    path('', EnterpriseListView2.as_view(), name='enterprise-list'),
    path('create/', EnterpriseCreateView.as_view(), name='enterprise-create'),
    #path('<int:pk>/', EnterpriseDetailView.as_view(), name='enterprise-detail'),
    #path('<int:pk>/update/', EnterpriseUpdateView.as_view(), name='enterprise-update'),
    #path('<int:pk>/delete/', EnterpriseDeleteView.as_view(), name='enterprise-delete'),
    path('search/', SearchEntView.as_view(), name='enterprise-search'),
    
    ########
    path('<slug:slug>/', EnterpriseDetailView.as_view(), name='enterprise-detail'), 
    path('<slug:slug>/update/', EnterpriseUpdateView.as_view(), name='enterprise-update'),
    path('<slug:slug>/delete/', EnterpriseDeleteView.as_view(), name='enterprise-delete'),
    path('ajax/load-sectors/', load_industry, name='ajax-load-sectors'),
    #path('industry-json/', get_json_industry_data, name='industry-json'),
     
]