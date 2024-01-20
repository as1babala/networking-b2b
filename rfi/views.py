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

#from core.models import Projects
from .forms import *
from django.db.models import Count
from core.models import *
from django.shortcuts import render
import io
from django.http import FileResponse
#from .filters import ProjectFilter

class RfiListView(LoginRequiredMixin, generic.ListView):
    model = Rfi
    template_name = "rfi/rfi_list.html"
    queryset = Rfi.objects.all() # not adding context here
    context_object_name = "user_rfi"
    paginate_by = 2
    
class UserRfiListView(LoginRequiredMixin, generic.ListView):
    template_name = "rfi/rfi_user_list.html"
    context_object_name = "rfi"
    paginate_by = 2
    
    def get_queryset(self):
        return Rfi.objects.filter(client_name=self.request.user).order_by('-created_on')
    
class RfiDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "rfi/rfi_detail.html"
    queryset = Rfi.objects.all() # not adding context here
context_object_name = "rfi"

class RfiUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "rfi/rfi_update.html"
    form_class = RfiForm
    queryset = Rfi.objects.all()
    
    def get_success_url(self):
        return reverse("rfi:rfi-list") 
    
    def form_valid(self, form):
        form.save()
        messages.info(self.request, "You have successfully updated this lead")
        return super(RfiUpdateView, self).form_valid(form)
    
class RfiDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "rfi/rfi_delete.html"
    queryset = Rfi.objects.all()
    
    def get_success_url(self):
        return reverse("rfi:rfi-list")

