from itertools import count
from django.shortcuts import render, get_object_or_404
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

from django.http.response import HttpResponse

from core.models import Education
from .forms import *

from django.db.models import Count

# Create your views here.


class EducationListView(LoginRequiredMixin, generic.ListView):
    template_name = "education/education_list.html"
    queryset = Education.objects.all() # not adding context here
    context_object_name = "education"
    paginate_by = 2

class UserEducationListView(LoginRequiredMixin, generic.ListView):
    template_name = "education/education_user.html"
    queryset = Education.objects.all() # not adding context here
    context_object_name = "education"
    paginate_by = 2
     
class EducationDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "education/education_detail.html"
    queryset = Education.objects.all() # not adding context here
    context_object_name = "education"
    
class EducationCreateView(LoginRequiredMixin, CreateView):
    template_name = "education/education_create.html"
    form_class = EducationModelForm
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.email = self.request.user.email
        return super().form_valid(form)
    
    
    def get_success_url(self):
        return reverse("education:education-list")

class EducationUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "education/education_update.html"
    form_class = EducationModelForm
    queryset = Education.objects.all()
    
    def get_success_url(self):
        return reverse("education:education-list")
    
    
    def form_valid(self, form):
        form.save()
        messages.info(self.request, "You have successfully updated this lead")
        return super(EducationUpdateView, self).form_valid(form)
    
class EducationDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "education/education_delete.html"
    queryset = Education.objects.all()
    
    def get_success_url(self):
        return reverse("education:education-list")


class EducationSearchView(ListView):
    model = Education
    template_name = "education/education_search.html"
    paginate_by= 1

    def get_queryset(self):  # new
        query = self.request.GET.get("q")
        object_list = Education.objects.filter(
            Q(user_name__icontains=query) | 
            Q(school_name__icontains=query) | 
            Q(start_date__icontains=query)  |
            Q(end_date__icontains=query)  |
            Q(degree__icontains=query)|
            Q(specialization__icontains=query)|  
            Q(minor__icontains=query)
            
            )
        return object_list
        #return reverse( "Educations: Education-update")

#######
@login_required
def EducationSummary(request):
    qs = Education.objects.values('education').annotate(total_cnt=Count('id'))
    
    qs2 = Education.objects.values('school_name').annotate(total_cnt=Count('name'))
    qs3 = Education.objects.values('start_date').annotate(total_cnt=Count('id'))
    qs4 = Education.objects.values('degree').annotate(total_cnt=Count('id'), unique= Count('name', distinct=True))
    context = {
        'qs': qs,
        'qs2': qs2,
        'qs3': qs3,
        'qs4': qs4
    }
    return render (request, "education/education_report.html", context)

