from itertools import count
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.views.generic import (
    TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.decorators import user_passes_test
from django.http.response import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http.response import HttpResponse
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin

from django.core.mail import send_mail
#from slick_reporting.views import SlickReportView
#from slick_reporting.fields import SlickReportField
from core.models import *
from django.db.models import Count, Avg

class admin(UserPassesTestMixin):
    
    def test_func(self):
        return self.request.user.is_admin
    
class employee(UserPassesTestMixin):
    
    def test_func(self):
        return self.request.user.is_employee
       
class MainAnalyticsView(admin, employee, ListView):
    context_object_name = "data"
    template_name = "analytics/main.html"

    def get_queryset(self):
        my_set = {
        "blog_published": Blog.objects.filter(status="PUBLISHED").count(),
        "blog_drafted": Blog.objects.filter(status="DRAFT").count(),
        "blog_archived": Blog.objects.filter(status="ARCHIVED").count(),
        "experts": CustomUser.objects.filter(is_expert=True ).count(),
        "enterprises": Enterprises.objects.filter().count(),
        "blog_metrics": Blog.objects.values('status').annotate(count=Count("status")),# group_by() on status
        "reviews": Review.objects.values('rating').annotate(count=Count("rating")),
        "reviews_data": Review.objects.all(),
        "review_1": Review.objects.filter(rating = 5).count(),
        "blogs_with_review_counts": Blog.objects.annotate(review_count=Count('reviews')),
        "blogs_with_rating_average": Blog.objects.annotate(review_count=Avg('reviews'), average_rating=Avg('reviews__rating'))
        
           
        }
        return my_set
@login_required()
def main_analytics(request):
    blog_published = Blog.objects.filter(status="PUBLISHED").count()
    blog_drafted = Blog.objects.filter(status="DRAFT").count()
    blog_archived = Blog.objects.filter(status="ARCHIVED").count()
    experts= CustomUser.objects.filter(is_expert=True ).count()
    enterprises=Enterprises.objects.filter().count()
    reviews = Review.objects.values('rating').annotate(count=Count("reviews"), average_rating=Avg('ating'))
    context = {
        'blog_published': blog_published,
        'blog_drafted': blog_drafted,
        'blog_archived': blog_archived,
        'experts': experts,
        'enterprises': enterprises,
        'reviews': reviews
    }
    return render(request, 'analytics/main.html', context)