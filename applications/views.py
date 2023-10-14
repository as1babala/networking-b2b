from itertools import count
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.views.generic import (
    TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail

from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from core.models import *
from .forms import *
from django.db.models import Count


    
#### Job Application ####
class ApplicationsListView(LoginRequiredMixin, generic.ListView):
    template_name = "applications/application_list.html"
    queryset = JobApplication.objects.all() # not adding context here
    context_object_name = "applications"
    paginate_by = 2

@login_required
def UserApplicationsListView(request):
    applications = JobApplication.objects.filter(user=request.user) # not adding context here
    return render(request, 'applications/application_user_list.html', {'applications': applications})

 
class JobApplicationCreateView( CreateView):
    template_name = "applications/application_create.html"
    form_class = JobApplicationForm
    
    def get_success_url(self):
        return reverse("applications:application-list")
    
class JobSearchView(ListView):
    model = Jobs
    template_name = "applications/application_search.html"
    paginate_by= 1

    def get_queryset(self):  # new
        query = self.request.GET.get("q")
        object_list = JobApplication.objects.filter(
            Q(company_name__icontains=query) | 
            Q(job_grade__icontains=query)  |
            Q(Salary__icontains=query)  |
            Q(job_type__icontains=query)|
            Q(Department__icontains=query)|  
            Q(summary_since_hired__icontains=query)|
            Q(job_qualifications_since_hired__icontains=query)
            
            )
        return object_list    