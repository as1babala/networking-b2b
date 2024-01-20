from django.urls import path
from .views import *


app_name = 'blogs'

urlpatterns = [
    path('', BlogListView.as_view(), name='blog-list'),
    path('draft/', BlogDraftListView.as_view(), name='blog-draft'),
    path('archived/', BlogArchivedListView.as_view(), name='blog-archived'),
    #path('categories/', CategoryListView.as_view(), name='category-list'),
    path('<int:pk>/', blog_detail, name='blog-detail'),
    path('create/', BlogCreateView.as_view(), name='blog-create'),
    path('categories/create/', CategoryCreateView.as_view(), name='category-create'),
    path('<int:pk>/update/', BlogUpdateView.as_view(), name='blog-update'),
    path('<int:pk>/delete/', BlogDeleteView.as_view(), name='blog-delete'),
    #path('<int:pk>/review/', add_review, name='review-create'),
    path('<int:pk>/review/', ReviewCreateView.as_view(), name='review-create'),# for review
    #path('<int:pk>/', BlogDetailView.as_view(), name='blog-detail'),
    path('search/', BlogsSearchView.as_view(), name='blog-search'),
    path('review/<int:review_id>/reply/new/', send_reply, name='reply-create'), 
    #path('review/<int:review_id>/reply/new/', ReplyToReviewCreateView.as_view(), name='reply-create'),
    path('reply/<int:pk>/edit/', ReplyToReviewUpdateView.as_view(), name='reply-update'),
    path('reply/<int:pk>/delete/', ReplyToReviewDeleteView.as_view(), name='reply-delete'),
    path('read-history/', read_history, name='read-history'),
    path('categories/', category_list, name='category-list'),
    #path('categories/<slug:slug>/', category_detail, name='category-detail'),
    path('categories/<int:pk>/', category_detail, name='category-detail'),
]