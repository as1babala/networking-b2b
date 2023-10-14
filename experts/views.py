from itertools import count
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.views.generic import (
    TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.http.response import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http.response import HttpResponse

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail

#from slick_reporting.views import SlickReportView
#from slick_reporting.fields import SlickReportField

from core.models import *
from core.forms import *
from django.db.models import Count

# Create your views here.


class ExpertsListView(LoginRequiredMixin, generic.ListView):
    template_name = "experts/expert_list.html"
    queryset = Experts.objects.all() # not adding context here
    #queryset = CustomUser.objects.filter(user_type='Consultants') # not adding context here
    
    context_object_name = "experts"
    paginate_by = 4
    
class ExpertsDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "experts/expert_detail.html"
    queryset = Experts.objects.all() # not adding context here
    context_object_name = "experts"
    
@login_required
def expert_detail(request, pk):
    expert = Experts.objects.get(id=pk)
    context = {
        "expert": expert
    }
    return render(request, "experts/expert_detail.html", context)
    
class ExpertsCreateView(LoginRequiredMixin, CreateView):
    template_name = "experts/expert_create.html"
    form_class = ExpertForm
    
    def get_success_url(self):
        return reverse("experts:expert-list")

class ExpertsUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "experts/expert_update.html"
    form_class = ExpertForm
    queryset = Experts.objects.all()
    
    def get_success_url(self):
        return reverse("experts:expert-list")
    
    def form_valid(self, form):
        form.save()
        messages.info(self.request, "You have successfully updated this lead")
        return super(ExpertsUpdateView, self).form_valid(form)
    
class ExpertsDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "experts/expert_delete.html"
    queryset = Experts.objects.all()
    
    def get_success_url(self):
        return reverse("experts:expert-list")

def BootstrapFilterView(request):
    last_name_contains = request.GET.get('last_name')
    first_name_contains = request.GET.get('first_name')
    return


class SearchResultsView(ListView):
    model = Experts
    template_name = "experts:expert_search.html"
    paginate_by= 4

    def get_queryset(self):  # new
        query = self.request.GET.get("q")
        object_list = Experts.objects.filter(
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query)  |
            Q(DOB__icontains=query)  |
            Q(city__icontains=query)|
            Q(country__icontains=query)|  
            Q(created_on__icontains=query)|
            Q(id__icontains=query)
            
            )
        return object_list
        #return reverse( "consultants: consultant-update")

def expert_detail(request, pk):
    expert = Experts.objects.get(pk=pk)
    
    form = EducationModelForm()
    if request.method == 'POST':
        form = EducationModelForm(request.POST)
        if form.is_valid():
            education = Education(
                author=form.cleaned_data["author"],
                
                expert=expert
            )
            education.save()

    education = Education.objects.filter(expert=expert)
    context = {
        "expert": expert,
        "education": education,
        "form": form,
    }

    return render(request, "educations/education_detail.html", context)
