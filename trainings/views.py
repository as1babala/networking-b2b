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
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from core.models import *
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from core.forms import *
from django.db.models import Count



class admin(UserPassesTestMixin):
    
    def test_func(self):
        return self.request.user.is_admin
    
class employee(UserPassesTestMixin):
    
    def test_func(self):
        return self.request.user.is_employee
class TrainingListView( generic.ListView):
    template_name = "trainings/training_list.html"
    queryset = Trainings.objects.all() # not adding context here
    context_object_name = "trainings"
    paginate_by = 4
    
class TrainingCreateView(admin, employee, CreateView):
    template_name = "trainings/training_create.html"
    form_class = TrainingForm
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.email = self.request.user.email
        
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("trainings:training-list")

class TrainingDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "trainings/training_detail.html"
    queryset = Trainings.objects.all() # not adding context here
    context_object_name = "trainings"

class TrainingUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "trainings/training_update.html"
    form_class = TrainingForm
    queryset = Trainings.objects.all()
    
    def get_success_url(self):
        return reverse("trainings:training-list")
     
    def form_valid(self, form):
        form.save()
        messages.info(self.request, "You have successfully updated this lead")
        return super(TrainingUpdateView, self).form_valid(form)
    
class TrainingDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "trainings/training_delete.html"
    queryset = Trainings.objects.all()
    
    def get_success_url(self):
        return reverse("trainings:training-list")
    
    
class MemberApplicationCreateView( LoginRequiredMixin, CreateView):
    model = TrainingApplication
    fields = [ 'phone_code','phone_number', 'member', 'position']
    template_name = "trainingapplications/application_create.html"
    success_url = reverse_lazy('trainings:training-list')
     
    def form_valid(self, form):
        form.instance.name = self.request.user.last_name
        form.instance.email = self.request.user.email
        form.instance.company_name = self.request.user.company_name
        form.instance.training = Trainings.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

class NewApplicationCreateView( CreateView):
    model = TrainingApplication
    fields = [ 'name','email','company_name','phone_code','phone_number', 'member', 'position']
    template_name = "trainingapplications/application_create.html"
    success_url = reverse_lazy('trainings:training-list')
     
    def form_valid(self, form):
        form.instance.name = self.request.user.last_name
        form.instance.email = self.request.user.email
        form.instance.company_name = self.request.user.company_name
        form.instance.training = Trainings.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)   

class TrainingSearchView(ListView):
    model = Trainings
    template_name = "trainings/training_search.html"
    paginate_by= 2

    def get_queryset(self):  # new
        query = self.request.GET.get("q")
        object_list = Trainings.objects.filter(
            
            Q(teacher__icontains=query)|
            Q(training_title__icontains=query)|
            Q(domain__icontains=query)|
            Q(email__icontains=query)|
            Q(cost__icontains=query)|
            Q(training_mode__icontains=query)|
            Q(duration__icontains=query)
            
            )
        return object_list 