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
from core.forms import *
from django.db.models import Count

class TrainingApplicationListView( generic.ListView):
    template_name = "trainingapplications/training_application_list.html"
    queryset = TrainingApplication.objects.all() # not adding context here
    context_object_name = "applications"
    paginate_by = 4

class UserTrainingApplicationListView( generic.ListView):
    template_name = "trainingapplications/user_training_application_list.html"
    context_object_name = "user_applications"
    paginate_by = 4 
    
    def get_queryset(self):
        return TrainingApplication.objects.filter(name=self.request.user).order_by('-created_on')
   
class TrainingApplicationDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "trainingapplications/training_application_detail.html"
    queryset = TrainingApplication.objects.all() # not adding context here
    context_object_name = "applications"
    
class TrainingApplicationDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "trainingapplications/training_application_detail.html"
    queryset = TrainingApplication.objects.all() # not adding context here
    context_object_name = "applications"
    
class TrainingApplicationUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "trainingapplications/training_application_update.html"
    form_class = TrainingApplicationForm
    queryset = TrainingApplication.objects.all()
    
    def get_success_url(self):
        return reverse("trainingapplications:training-app-list")
     
    def form_valid(self, form):
        form.save()
        messages.info(self.request, "You have successfully updated this lead")
        return super(TrainingApplicationUpdateView, self).form_valid(form)