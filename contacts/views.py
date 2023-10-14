from django.shortcuts import render
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

#from slick_reporting.views import SlickReportView
#from slick_reporting.fields import SlickReportField

from accounts.models import *
from core.forms import *
from django.db.models import Count

# Create your views here.


class ContactListView(LoginRequiredMixin, generic.ListView):
    template_name = "contacts/contact_list.html"
    queryset = ContactUs.objects.all() # not adding context here
    context_object_name = "contacts"
    paginate_by = 2
    
class ContactDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "contacts/contact_detail.html"
    queryset = ContactUs.objects.all() # not adding context here
    context_object_name = "contacts"

    
class ContactCreateView( CreateView):
    template_name = "contacts/contact_create.html"
    form_class = ContactusForm
    
    def get_success_url(self):
        return reverse("contacts:contact-list")


class SearchContactView(ListView):
    model = ContactUs
    template_name = "contacts/contact_search.html"
    paginate_by= 1

    def get_queryset(self):  # new
        query = self.request.GET.get("q")
        object_list = ContactUs.objects.filter(
            Q(name__icontains=query) | 
            Q(email__icontains=query)  |
            Q(phone_ind__icontains=query)  |
            Q(phone_number__icontains=query)|
            Q(created_on__icontains=query)
            )
        return object_list

   