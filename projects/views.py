from itertools import count
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.views.generic import (
    TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.template.loader import get_template
#from slick_reporting.views import SlickReportView
#from slick_reporting.fields import SlickReportField

from core.models import Projects
from .forms import *
from django.db.models import Count

from django.shortcuts import render
import io
from django.http import FileResponse
from .filters import ProjectFilter
#from reportlab.pdfgen import canvas


# Create your views here.
class ProjectListView(LoginRequiredMixin, generic.ListView):
    model = Projects
    template_name = "projects/project_list.html"
    #queryset = Projects.objects.all() # not adding context here
    #context_object_name = "projects"
    paginate_by = 2
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ProjectFilter(self.request.GET, queryset=self.get_queryset())
        #context['filter'] = self.ProjectFilter(self.request.GET, queryset=self.get_queryset())
        return context
    
class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "projects/project_detail.html"
    queryset = Projects.objects.all() # not adding context here
    context_object_name = "projects"
    
class ProjectCreateView(LoginRequiredMixin, CreateView):
    template_name = "projects/project_create.html"
    form_class = ProjectsForm
    
    def get_success_url(self):
        return reverse("projects:project-list")
    
# Multi-level create views
@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectsForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            form.instance.project_initiator = request.user
            # Set the reviewer and approver here if needed or leave them to be set later
            project.save()
            messages.success(request, 'Project created successfully!')
            #return redirect('projects:project-detail', pk=project.pk)
            return redirect('projects:project-list')
    else:
        form = ProjectsForm()
    return render(request, 'projects/project_create.html', {'form': form})


@login_required
def review_project(request, pk):
    project = get_object_or_404(Projects, pk=pk)
    if request.method == 'POST':
        form = ProjectReviewedForm(request.POST, instance=project)
        if form.is_valid():
            form.instance.reviewed_by = request.user
            form.save()
            messages.success(request, 'Project reviewed successfully!')
            #return redirect('projects:project-update', pk=project.pk)
            return redirect('projects:project-list')
    else:
        form = ProjectReviewedForm(instance=project)
    return render(request, 'projects/project_review.html', {'form': form, 'project': project})

@login_required
def approve_project(request, pk):
    project = get_object_or_404(Projects, pk=pk)
    if not project.reviewed:
        messages.error(request, 'Project must be reviewed before approval.')
        return redirect('projects:project-list', pk=project.pk)
        #return redirect('projects:project-list')
    
    if request.method == 'POST':
        form = ProjectApprovedForm(request.POST, instance=project)
        if form.is_valid():
            form.instance.approved_by = request.user
            form.save()
            messages.success(request, 'Project approval status updated!')
            #return redirect('projects:project-list', pk=project.pk)
            return redirect('projects:project-list')
    else:
        form = ProjectApprovedForm(instance=project)
    return render(request, 'projects/project_approve.html', {'form': form, 'project': project})



class ProjectUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "projects/project_update.html"
    form_class = ProjectsForm
    queryset = Projects.objects.all()
    
    def get_success_url(self):
        return reverse("projects:project-list") 
    
    def form_valid(self, form):
        form.save()
        messages.info(self.request, "You have successfully updated this lead")
        return super(ProjectUpdateView, self).form_valid(form)
    
class ProjectDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "projects/project_delete.html"
    queryset = Projects.objects.all()
    
    def get_success_url(self):
        return reverse("projects:project-list")


class SearchProjectView(ListView):
    model = Projects
    template_name = "projects/project_search.html"
    paginate_by= 1

    def get_queryset(self):  # new
        query = self.request.GET.get("q")
        object_list = Projects.objects.filter(
            Q(company_name__icontains=query) | 
            Q(project_name__icontains=query)  |
            Q(review__icontains=query)  |
            Q(reviewer__icontains=query)|
            Q(approver__icontains=query)|  
            Q(create_on__icontains=query)
            
            )
        return object_list
        
def ProjectDocumentUpload(request, parent_id=None):
    form = ProjectDocumentUploadForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.document = parent_id
        obj.save()
        return render(request, "project_document.html", {"form":form})
        

### Project pending for review ###
class NotReviewedListView(LoginRequiredMixin, generic.ListView):
    template_name = "projects/project_notreviewed.html"
    queryset = Projects.objects.filter(reviewed=False) # not adding context here
    context_object_name = "notreviewed"
    paginate_by = 2
    
### Project pending for approval ###
class ReviewedListView(LoginRequiredMixin, generic.ListView):
    template_name = "projects/project_reviewed.html"
    queryset = Projects.objects.filter(reviewed=True, approved=False) # not adding context here
    context_object_name = "reviewed"
    paginate_by = 2
    

### Project approved ###
class ApprovedListView(LoginRequiredMixin, generic.ListView):
    template_name = "projects/project_approved.html"
    queryset = Projects.objects.filter(reviewed=True, approved=True) # not adding context here
    context_object_name = "approved"
    paginate_by = 2
    

### Project Rejected ###
class RejectedListView(LoginRequiredMixin, generic.ListView):
    template_name = "projects/project_rejected.html"
    queryset = (Projects.objects.filter(reviewed=False) | Projects.objects.filter(approved=False)) # not adding context here
    context_object_name = "rejected"
    paginate_by = 2  

