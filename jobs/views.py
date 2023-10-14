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
from core.models import *
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .forms import *
from django.db.models import Count

class JobListView( generic.ListView):
    template_name = "jobs/job_list.html"
    queryset = Jobs.objects.all() # not adding context here
    context_object_name = "jobs"
    paginate_by = 2
    
class JobCreateView(LoginRequiredMixin, CreateView):
    template_name = "jobs/job_create.html"
    form_class = JobForm
    
    def form_valid(self, form):
        form.instance.job_contact = self.request.user
        form.instance.email = self.request.user.email
        form.instance.company_name = self.request.user.company_name
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("jobs:job-list")

class JobDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "jobs/job_detail.html"
    queryset = Jobs.objects.all() # not adding context here
    context_object_name = "jobs"

class JobUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "jobs/job_update.html"
    form_class = JobForm
    queryset = Jobs.objects.all()
    
    def get_success_url(self):
        return reverse("jobs:job-list")
     
    def form_valid(self, form):
        form.save()
        messages.info(self.request, "You have successfully updated this lead")
        return super(JobUpdateView, self).form_valid(form)
    
class JobDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "jobs/job_delete.html"
    queryset = Jobs.objects.all()
    
    def get_success_url(self):
        return reverse("jobs:job-list")
    
    
class ApplicationCreateView( LoginRequiredMixin, CreateView):
    model = JobApplication
    fields = [ 'resume', 'cover_letter']
    template_name = "applications/application_create.html"
    success_url = reverse_lazy('jobs:job-list')
     
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.email = self.request.user.email
        form.instance.job = Jobs.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

    
class ApplicationResumeUploadView(generic.View):
    def get(self, request, pk):
        application = get_object_or_404(JobApplication, pk=pk)
        form = JobApplicationForm(instance=application)
        return render(request, 'jobs/application_resume_form.html', {'form': form})
    
    def post(self, request, pk):
        application = get_object_or_404(JobApplication, pk=pk)
        form = JobApplicationForm(request.POST, request.FILES, instance=application)
        if form.is_valid():
            form.save()
            return redirect('application_detail', pk=pk)
        return render(request, 'jobs/application_resume_form.html', {'form': form})

    
    #def get_success_url(self):
        #return reverse("applications:application-list")
class ApplicationDeleteView(LoginRequiredMixin, CreateView):
    def get(self, request, pk):
        application = get_object_or_404(JobApplication, pk=pk)
        return render(request, 'jobs/application_confirm_delete.html', {'application': application})     
    
    def post(self, request, pk):
        application = get_object_or_404(JobApplication, pk=pk)
        job_pk = application.job.pk
        application.delete()
        return redirect('job_detail', pk=job_pk)

     
class JobSearchView(ListView):
    model = Jobs
    template_name = "jobs/job_search.html"
    paginate_by= 2

    def get_queryset(self):  # new
        query = self.request.GET.get("q")
        object_list = Jobs.objects.filter(
            Q(company_name__icontains=query)| 
            Q(job_grade__icontains=query)  |
            Q(Salary__icontains=query)  |
            Q(job_type__icontains=query)|
            Q(country__icontains=query)|
            Q(city__icontains=query)|
            Q(Department__icontains=query)|  
            Q(summary__icontains=query)|
            Q(travel_required__icontains=query)|
            Q(job_qualifications__icontains=query)
            
            )
        return object_list
        
        
### create application###
@login_required
def apply_job(request, pk, format=None):
    job = Jobs.objects.get(id=pk)
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            resume = form.cleaned_data['resume']
            email = form.cleaned_data['email']
            cover_letter = form.cleaned_data['cover_letter']
            JobApplication.objects.create(full_name=full_name, job=job, resume=resume, cover_letter=cover_letter)
            return redirect('applications:application-list')
    else:
        form = JobApplicationForm()
    return render(request, 'applications/application_create.html', {'form': form, 'job': job})
   
@login_required
def apply_for_job(request, pk, format=None):
    job = Jobs.objects.get(id=pk)
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.instance.user = request.user
            #application.email= request.user.email
            #application.job = job
            application.save()
            return redirect('job_detail', pk=pk)
    else:
        form = JobApplicationForm()
    return render(request, 'applications/application_create.html', {'form': form, 'job': job})


