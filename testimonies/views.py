from itertools import count
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.views.generic import (
    TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http.response import HttpResponse

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.urls import reverse_lazy
#from slick_reporting.views import SlickReportView
#from slick_reporting.fields import SlickReportField

from core.models import *
from .forms import *
from django.db.models import Count

# Create your views here.


class TestimonyListView(LoginRequiredMixin, generic.ListView):
    template_name = "testimonies/testimony_list.html"
    queryset = Testimonies.objects.all() # not adding context here
    context_object_name = "testimony"
    paginate_by = 2
    
class TestimonyDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "testimonies/testimony_detail.html"
    queryset = Testimonies.objects.all() # not adding context here
    context_object_name = "testimony"  
    
class TestimonyCreateViewi(LoginRequiredMixin, CreateView):
    template_name = "testimonies/testimony_create.html"
    form_class = TestimonyForm
    
    def get_success_url(self):
        return reverse("testimony:testimony-list")

class TestimonyCreateView( LoginRequiredMixin, CreateView):
    model = Testimonies
    fields = [ 'title','testimony']
    template_name = "testimonies/testimony_create.html"
    success_url = reverse_lazy('testimonies:testimony-list')
     
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    


class TestimonyDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "testimonies/testimony_detail.html"
    queryset = Testimonies.objects.all() # not adding context here
    context_object_name = "testimony"

class TestimonySearchView(ListView):
    model = Testimonies
    template_name = "testimonies/testimony_search.html"
    paginate_by= 1

    def get_queryset(self):  # new
        query = self.request.GET.get("q")
        object_list = Testimonies.objects.filter(
            Q(title__icontains=query) | 
            Q(user__icontains=query)  |
            Q(created_at__icontains=query)  
            
           
            )
        return object_list
 