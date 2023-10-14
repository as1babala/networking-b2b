from django.urls import path
from .views import *


app_name = 'profiles'

urlpatterns = [
    path('' , profile_page, name='user-profile'),
    path('expert_profile/' , expert_profile_view, name='expert-profile'),
    path('employee_profile/' , employee_profile_view, name='employee-profile'),
    path('company_profile/' , company_profile_view, name='company-profile'),
    
    path('admin_profile/' , admin_profile_view, name='admin-profile'),
]