from django.urls import path
from .views import *


app_name = 'profiles'

urlpatterns = [
    #path('' , profile_page, name='user-profile'),
    path('expert_profile/' , view_profile, name='expert-profile'),
    path('employee_profile/' , employee_profile_view, name='employee-profile'),
    path('admin_profile/' , admin_profile_view, name='admin-profile'),
    path('expert_profile_list/' , ExpertProfileListView.as_view(), name='expert-profile-list'),
    path('<int:pk>/', ExpertProfileDetailView.as_view(), name='expert-profile-detail'),
    #path('<int:pk>/update/', ExpertProfileUpdateView.as_view(), name='expert-profile-update'),
    path('<int:pk>/delete/', ExpertProfileDeleteView.as_view(), name='expert-profile-delete'),
    path('user/', ExpertUserProfileListView.as_view(), name='expert-user-profile-list'),
    
    path('<slug>/', ExpertProfileDetailView.as_view(), name='expert-profile-detail'),
    path('<slug>/update/', ExpertProfileUpdateView.as_view(), name='expert-profile-update'),
    #path('<slug>/delete/', ExpertProfileDeleteView.as_view(), name='expert-profile-delete'),
    path('expert/search/', ExpertProfileSearchView.as_view(), name='expert-profile-search'),
    #path('<slug>/', ExpertProfileDetailView.as_view(), name='expert-portfolio-detail'),
    #path('<int:pk>/', profile_info, name='expert-profile-detail'),
    #path('expert/message/create/', ExpertMessagingCreateView.as_view(), name='expert-message-create'),
    
    path('expert/message/<int:expert_id>/', send_message, name='expert-message-create'),
    path('expert/messages/', ExpertMessageListView.as_view(), name='expert-message-list'),
    path('expert/messages/received', ExpertMessageReceivedListView.as_view(), name='expert-received-message-list'),
    path('expert/messages/sent', ExpertMessageSentListView.as_view(), name='expert-sent-message-list'),
    
    path('admin-profile-list/' , AdminProfileListView.as_view(), name='admin-profile-list'),
    
]

