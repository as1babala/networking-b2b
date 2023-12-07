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
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.forms import modelformset_factory
from core.models import *
from .forms import *
from rfi.forms import *
from django.db.models import Count

class admin(UserPassesTestMixin):
    
    def test_func(self):
        return self.request.user.is_admin
    
class employee(UserPassesTestMixin):
    
    def test_func(self):
        return self.request.user.is_employee

class DealsListView(LoginRequiredMixin, generic.ListView):
    template_name = "deals/deal_list.html"
    queryset = Deals.objects.all() # for published blogs
    #queryset = Blog.objects.all().filter(status=2)
    #queryset = Blog.objects.all()
    #queryset = CustomUser.objects.filter(user_type='blog') # not adding context here
    #CustomUser.objects.
    context_object_name = "deals"
    paginate_by = 4

class UserDealsListView(LoginRequiredMixin, generic.ListView):
    template_name = "deals/deal_user_list.html"
    context_object_name = "user_deals"
    
    def get_queryset(self):
        return Deals.objects.filter(dealer=self.request.user).order_by('-created_on')

class DealCreateView1(LoginRequiredMixin, CreateView):
    template_name = "deals/deal_create.html"
    form_class = DealsForm
    form_class2 = DealImagesForm
    success_url = reverse_lazy('deals:deal-list')
    
     
    def form_valid(self, form):
        form.instance.dealer = self.request.user
        form.instance.email = self.request.user.email
        form.instance.company_name = self.request.user.company_name
        messages.success(self.request, f'Your account has been created! You are now able to log in')
            
        return super().form_valid(form)
class DealCreateView(LoginRequiredMixin, CreateView):
    model = Deals
    form_class = DealsForm
    template_name = 'deals/deal_create.html'
    success_url = reverse_lazy('deals:deal-list')  # Replace 'thanks' with your success URL name

    def form_valid(self, form):
        # Deal instance
        self.object = form.save(commit=False)
        self.object.dealer = self.request.user
        self.object.email = self.request.user.email
        self.object.company_name = self.request.user.company_name
        self.object.save()

        # DealImages instances
        images = self.request.FILES.getlist('image')
        for image in images:
            DealImages.objects.create(deal=self.object, image=image)

        return redirect(self.get_success_url())

### Create view with pictures
def deal_create(request):
    form = DealsForm()
    form2 = DealImagesForm()

    if request.method == 'POST':
        form = DealsForm(request.POST)
        form2 = DealImagesForm(request.POST, request.FILES)
        images = request.FILES.getlist('image')
        if form.is_valid() and form2.is_valid():
            form.instance.dealer = request.user
            form.instance.email = request.user.email
            form.instance.company_name = request.user.company_name
            #dealer = form.cleaned_data['dealer']
            #email = form.cleaned_data['email']
            #company_name = form.cleaned_data['company_name']
            service_category = form.cleaned_data['service_category']
            deal_title = form.cleaned_data['deal_title']
            deal_country = form.cleaned_data['deal_country']
            deal_city = form.cleaned_data['deal_city']
            deal_type = form.cleaned_data['deal_type']
            descriptions = form.cleaned_data['descriptions']
            active = form.cleaned_data['active']  
    
            
            deal_instance = Deals.objects.create(dealer=request.user, email=request.user.email, company_name=request.user.company_name, service_category=service_category, deal_title=deal_title, deal_country=deal_country, deal_city=deal_city, deal_type=deal_type, active=active, descriptions=descriptions
            )
            print('-------------------------------------------')
            print(deal_instance)
            print('-------------------------------------------')

            for i in images:
                DealImages.objects.create(deal=deal_instance, image=i)
            return redirect('thanks')

    context = {'form': form, 'form2': form2}
    return render(request, 'deals/deal_create.html', context)
    
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
    context_object_name = "delete_deals"
    
    def get_success_url(self):
        return reverse("deals:deal-list")


class RfiCreateView1( LoginRequiredMixin, CreateView):
    model = Rfi
    fields = [ 'message']
    template_name = "rfi/rfi_create.html"
    success_url = reverse_lazy('deals:deal-list')
     
    def form_valid(self, form):
        form.instance.client_name = self.request.user
        form.instance.client_email = self.request.user.email
        form.instance.deal = Deals.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)
    

class RfiCreateView( LoginRequiredMixin, CreateView):
    model = Rfi
    fields = [ 'message']
    template_name = "rfi/rfi_create.html"
    success_url = reverse_lazy('deals:deal-list')
     
    def form_valid(self, form):
        form.instance.client_name = self.request.user
        form.instance.client_email = self.request.user.email
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
            Q(service_category__icontains=query)|
            Q(deal_type__icontains=query) |
            Q(deal_title__icontains=query) |
            Q(active__icontains=query) |
            Q(created_on__icontains=query)
        )
        return object_list   
    