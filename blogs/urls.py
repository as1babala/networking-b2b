from django.urls import path
from .views import *


app_name = 'blogs'

urlpatterns = [
    path('', BlogListView.as_view(), name='blog-list'),
    path('draft/', BlogDraftListView.as_view(), name='blog-draft'),
    path('categories/', BlogListView.as_view(), name='category-list'),
    path('<int:pk>/', blog_detail, name='blog-detail'),
    path('create/', BlogCreateView.as_view(), name='blog-create'),
    path('categories/create/', CategoryCreateView.as_view(), name='category-create'),
    path('<int:pk>/update/', BlogUpdateView.as_view(), name='blog-update'),
    path('<int:pk>/delete/', BlogDeleteView.as_view(), name='blog-delete'),
    #path('<int:pk>/review/', add_review, name='review-create'),
    path('<int:pk>/review/', ReviewCreateView.as_view(), name='review-create'),# for review
    #path('<int:pk>/', BlogDetailView.as_view(), name='blog-detail'),
    path('search/', BlogsSearchView.as_view(), name='blog-search'),
]