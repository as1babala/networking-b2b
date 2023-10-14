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
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail

#from slick_reporting.views import SlickReportView
#from slick_reporting.fields import SlickReportField

from core.models import *
from .forms import *
from rfi.forms import *
from django.db.models import Count


class DealsListView(LoginRequiredMixin, generic.ListView):
    template_name = "deals/deal_list.html"
    queryset = Deals.objects.all() # for published blogs
    #queryset = Blog.objects.all().filter(status=2)
    #queryset = Blog.objects.all()
    #queryset = CustomUser.objects.filter(user_type='blog') # not adding context here
    #CustomUser.objects.
    context_object_name = "deals"
    paginate_by = 4



class DealCreateView(LoginRequiredMixin, CreateView):
    template_name = "deals/deal_create.html"
    form_class = DealsForm
    success_url = reverse_lazy('deals:deal-list')
    
     
    def form_valid(self, form):
        form.instance.dealer = self.request.user
        form.instance.email = self.request.user.email
        form.instance.company_name = self.request.user.company_name
        return super().form_valid(form)
    
def deal_detail(request, pk):
    deal = Deals.objects.get(pk=pk)
    
    form = RfiForm()
    if request.method == 'POST':
        form = RfiForm(request.POST)
        if form.is_valid():
            reviews = Rfi(
                email=form.cleaned_data["email"],
                company_name=form.cleaned_data["company_name"],
                deal_title=form.cleaned_data["deal_title"],
                deal_type=form.cleaned_data["deal_type"],
                descriptions=form.cleaned_data["descriptions"],
                deal=deal
            )
            reviews.save()

    rfi = Rfi.objects.filter(deal=deal)
    context = {
        "deal": deal,
        "rfi": rfi,
        "form": form,
    }

    return render(request, "deals/deal_detail.html", context)
  
class DealDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "deals/deal_detail.html"
    queryset = Deals.objects.all() # not adding context here
    context_object_name = "deals"
    

class DealUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "deals/deal_update.html"
    form_class = DealsForm
    queryset = Deals.objects.all()
    
    def get_success_url(self):
        return reverse("deals:deal-list")
    
    
    def form_valid(self, form):
        form.save()
        messages.info(self.request, "You have successfully updated this lead")
        return super(DealUpdateView, self).form_valid(form)
    

  
class DealDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "deals/deal_delete.html"
    queryset = Deals.objects.all()
    
    def get_success_url(self):
        return reverse("deals:deal-list")


class RfiCreateView1( LoginRequiredMixin, CreateView):
    model = Rfi
    fields = [ 'message']
    template_name = "rfi/rfi_create.html"
    success_url = reverse_lazy('deals:deal-list')
     
    def form_valid(self, form):
        form.instance.name = self.request.user
        form.instance.email = self.request.user.email
        form.instance.deal = Deals.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)
    

class RfiCreateView( LoginRequiredMixin, CreateView):
    model = Rfi
    fields = [ 'message']
    template_name = "rfi/rfi_create.html"
    success_url = reverse_lazy('deals:deal-list')
     
    def form_valid(self, form):
        form.instance.name = self.request.user
        form.instance.email = self.request.user.email
        form.instance.deal = Deals.objects.get(pk=self.kwargs['pk'])
        
        return super().form_valid(form)


class DealsSearchView(ListView):
    model = Deals
    template_name = "deals/deal_search.html"

    def get_queryset(self):  # new
        query = self.request.GET.get("q")
        object_list = Deals.objects.filter(
            
            #Q(dealer__icontains=query)| 
            Q(email__icontains=query)  |
            Q(company_name__icontains=query) |
            Q(category__icontains=query)|
            Q(deal_type__icontains=query) |
            Q(deal_title__icontains=query) |
            Q(active__icontains=query) |
            Q(created_on__icontains=query)
        )
        return object_list   
    