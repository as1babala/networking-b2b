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

# Create your views here.


class EducationListView(LoginRequiredMixin, generic.ListView):
    template_name = "education/education_list.html"
    queryset = Education.objects.all() # not adding context here
    context_object_name = "educations"
    paginate_by = 2

@login_required
def UserEducationListView(request):
    education = Education.objects.filter(user=request.user) # not adding context here
    return render(request, 'education/education_user.html', {'education': education})
    
    
    
@login_required
def EducationCreate(request):
    if request.method == 'POST':
        form = EducationModelForm(request.POST)
        if form.is_valid():
            education = form.save(commit=False)
            education.user = request.user
            education.save()
            return redirect('education:education-list')
    else:
        form = EducationModelForm()
    return render(request, 'education/education_create.html', {'form': form})

class EducationCreateView(LoginRequiredMixin, CreateView):
    template_name = "education/education_create.html"
    form_class = EducationModelForm
    success_url = reverse_lazy('education:education-list')
    
     
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.email = self.request.user.email
        return super().form_valid(form)
    
    
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