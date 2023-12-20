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
from .filters import *

class ProductDealsListView(ListView):
    model = ProductDeals
    template_name = 'product_deals/product_deals.html'
    context_object_name = 'deals'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        deals_with_images = []
        for deal in context['deals']:
            images = ProductDealImages.objects.filter(deal=deal)
            if images.exists():
                deal.image_url = images.first().image.url
            else:
                deal.image_url = None  # Placeholder if no image exists
            deals_with_images.append(deal)
        context['deals'] = deals_with_images
        context['filter'] = ProductDealsFilter(self.request.GET, queryset=self.get_queryset())
        return context
    

class UserProductDealsListView(LoginRequiredMixin, generic.ListView):
    template_name = "product_deals/product_deals_user.html"
    context_object_name = "deals"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        deals_with_images = []
        for deal in context['deals']:
            images = ProductDealImages.objects.filter(deal=deal)
            if images.exists():
                deal.image_url = images.first().image.url
            else:
                deal.image_url = None  # Placeholder if no image exists
            deals_with_images.append(deal)
        context['deals'] = deals_with_images
        context['filter'] = ProductDealsFilter(self.request.GET, queryset=self.get_queryset())
        return context
    
    def get_queryset(self):
        return ProductDeals.objects.filter(dealer=self.request.user).order_by('-announcement_date')

class ProductDealCreateView1(LoginRequiredMixin, CreateView):
    template_name = "product_deals/product_deals_create.html"
    form_class = ProductDealsForm
    success_url = reverse_lazy('product_deals:product-deal-list')
    
     
    def form_valid(self, form):
        form.instance.dealer = self.request.user
        form.instance.email = self.request.user.email
        form.instance.company_name = self.request.user.company_name
        messages.success(self.request, f'Your account has been created! You are now able to log in')
            
        return super().form_valid(form)
class ProductDealCreateView(LoginRequiredMixin, CreateView):
    model = ProductDeals
    form_class = ProductDealsForm
    template_name = 'product_deals/product_deals_create.html'
    success_url = reverse_lazy('product_deals:product-deal-list')  # Replace 'thanks' with your success URL name

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
            ProductDealImages.objects.create(deal=self.object, image=image)
        messages.success(self.request, f'Your announcement has been created! Stay tune to make sure you track all requests for a quick reply to your announcement')
        return redirect(self.get_success_url())
    
      
def product_deal_detail(request, pk):
    product_deal = ProductDeals.objects.get(pk=pk)
    user = request.user
    if not ProductDealRead.objects.filter(reader=user, product_deal_read=product_deal).exists():
        ProductDealRead.objects.create(reader=user, product_deal_read=product_deal) 
    form = ProductRFIForm()
    if request.method == 'POST':
        form = ProductRFIForm(request.POST)
        if form.is_valid():
            reviews = ProductRFI(
                email=form.cleaned_data["email"],
                company_name=form.cleaned_data["company_name"],
                product_title=form.cleaned_data["deal_title"],
                deal_type=form.cleaned_data["deal_type"],
                descriptions=form.cleaned_data["descriptions"],
                product_deal=product_deal
            )
            reviews.save()

    product_rfi = ProductRFI.objects.filter(product_deal=product_deal)
    deal_images = ProductDealImages.objects.filter(deal=product_deal)
    context = {
        "product_deal": product_deal,
        "product_rfi": product_rfi,
        "form": form,
        "deal_images": deal_images,
    }

    return render(request, "product_deals/product_deals_detail.html", context)

def product_deal_read_history(request):
    # Assuming you have the user object available
    return render(request, 'product_deals/product_deal_read_history.html', {'reader': request.user})

class ProductDealUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "product_deals/product_deals_update.html"
    form_class = ProductDealsForm
    queryset = ProductDeals.objects.all()
    #context_object_name = "product_deals"
    
    def get_success_url(self):
        return reverse("product_deals:product-deal-list")
    
    
    def form_valid(self, form):
        form.save()
        messages.info(self.request, "You have successfully updated this lead")
        return super(ProductDealUpdateView, self).form_valid(form)
    

class ProductDealDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "product_deals/product_deal_delete.html"
    queryset = ProductDeals.objects.all()
    
    def get_success_url(self):
        return reverse("product_deals:product-deal-list")
    

class ProductRFICreateView( LoginRequiredMixin, CreateView):
    model = ProductRFI
    fields = [ 'message']
    template_name = "product_deals/product_rfi_create.html"
    success_url = reverse_lazy('product_deals:product-deal-list')
     
    def form_valid(self, form):
        form.instance.client_name = self.request.user
        form.instance.client_email = self.request.user.email
        form.instance.product_deal = ProductDeals.objects.get(pk=self.kwargs['pk'])
        
        return super().form_valid(form)
    
### Product RFI ###

class ProductRFIListView(LoginRequiredMixin, generic.ListView):
    model = ProductRFI
    template_name = "product_deals/product_rfi_list.html"
    queryset = Rfi.objects.all() # not adding context here
    context_object_name = "product_rfi"
    paginate_by = 2
    
class ProductUserRfiListView(LoginRequiredMixin, generic.ListView):
    template_name = "product_deals/product_user_rfi_list.html"
    context_object_name = "product_user_rfi"
    paginate_by = 2
    
    def get_queryset(self):
        return ProductRFI.objects.filter(client_name=self.request.user).order_by('-created_on')
    
class ProductRfiDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "product_deals/product_rfi_detail.html"
    queryset = ProductRFI.objects.all() # not adding context here
    context_object_name = "product_rfi"

class RfiUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "product_deals/product_rfi_update.html"
    form_class = RfiForm
    queryset = Rfi.objects.all()
    
    def get_success_url(self):
        return reverse("product_deals:product-rfi-list") 
    
    def form_valid(self, form):
        form.save()
        messages.info(self.request, "You have successfully updated this lead")
        return super(RfiUpdateView, self).form_valid(form)
    
class RfiDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "rfi/rfi_delete.html"
    queryset = Rfi.objects.all()
    
    def get_success_url(self):
        return reverse("rfi:rfi-list")

class ProductDealsSearchView(ListView):
    model = ProductDeals
    template_name = "product_deals/product_deal_search.html"

    def get_queryset(self):  # new
        query = self.request.GET.get("q")
        object_list = ProductDeals.objects.filter(
            
            Q(dealer__icontains=query)| 
            Q(email__icontains=query) |
            Q(company_name__icontains=query)|
            Q(product_name__icontains=query) |
            Q(product_category__icontains=query) |
            Q(city__icontains=query)|
            Q(country__icontains=query) 
           
        )
        return object_list   
