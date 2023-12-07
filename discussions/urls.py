from django.urls import path
from .views import *


app_name = 'discussions'

urlpatterns = [
   
    path('', ForumListView.as_view() , name='forum-list'),
    path('create/', ForumCreateView.as_view() , name='forum-create'), 
    #path('<int:pk>/', ForumDetailView, name='forum-detail'),
    path('<int:pk>/', forum_detail, name='forum-detail'),
    path('<int:pk>/update/', ForumUpdateView.as_view(), name='forum-update'),
    path('<int:pk>/delete/', ForumDeleteView.as_view(), name='forum-delete'),
    path('<int:pk>/discussion/', DiscussionsCreateView.as_view(), name='discussion-create'),# for review
    path('users/', UserForumListView.as_view(), name='forum-user'),
     path('search/', ForumsSearchView.as_view(), name='forum-search'),
]