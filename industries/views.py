from itertools import count
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.views.generic import (
    TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.http import Http404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
#from slick_reporting.views import SlickReportView
#from slick_reporting.fields import SlickReportField
from core.models import *
from .forms import *
from django.db.models import Count
# Create your views here.
from django.shortcuts import render, redirect
#from .forms import CSVImportForm
import csv

def import_csv(request):
    if request.method == 'POST':
        form = CSVImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file'].read().decode('utf-8').splitlines()
            csv_reader = csv.DictReader(csv_file)

            for row in csv_reader:
                Industry.objects.create(
                    name=row["name"],
                    description=row["description"]
                   
                )

            return redirect('success_page')  # Redirect to a success page
    else:
        form = CSVImportForm()

    return render(request, 'industries/import.html', {'form': form})

class IndustryListView(LoginRequiredMixin, generic.ListView):
    template_name = "industries/industry_list.html"
    queryset = Industry.objects.all() # not adding context here
    context_object_name = "industry"
    paginate_by = 2
    
class IndustryDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "industries/industry_detail.html"
    queryset = Industry.objects.all() # not adding context here
    context_object_name = "industry"
    
class IndustryCreateView(LoginRequiredMixin, CreateView):
    template_name = "industries/industry_create.html"
    form_class = IndustryForm
    
    def get_success_url(self):
        return reverse("industries:industry-list")

class IndustryUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "industries/industry_update.html"
    form_class = IndustryForm
    queryset = Industry.objects.all()
    
    def get_success_url(self):
        return reverse("industries:industry-list")
    
    
    def form_valid(self, form):
        form.save()
        messages.info(self.request, "You have successfully updated this lead")
        return super(IndustryUpdateView, self).form_valid(form)
    
class IndustryDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "industries/industry_delete.html"
    queryset = Industry.objects.all()
    
    def get_success_url(self):
        return reverse("industries:industry-list")


class SearchIndView(ListView):
    model = Industry
    template_name = "industries/industry_search.html"
    paginate_by= 1

    def get_queryset(self):  # new
        query = self.request.GET.get("q")
        object_list = Industry.objects.filter(
            Q(industry_name__icontains=query) 
           
            
            )
        return object_list
        #return reverse( "enterprises: enterprise-update")



@login_required
def industry_update(request, pk):
    industry = Industry.objects.get(id=pk)
    form = IndustryForm(instance=industry)
    if request.method == "POST":
        form = IndustryForm(request.POST, instance=industry)
        if form.is_valid():
            form.save()
            return redirect("industries:industry-list")
    context = {
        "form": form,
        "industry": industry
    }
    return render(request, "industries/industry_update.html", context)         


def detail(request, industry_id):
    try:
        industry = Industry.objects.get(pk=industry_id)
    except Industry.DoesNotExist:
        raise Http404("industry does not exist")
    return render(request, 'industries/industry_detail.html', {'industry': industry})


###### Sectors ########


class SectorListView(LoginRequiredMixin, generic.ListView):
    template_name = "industries/sector_list.html"
    queryset = Sectors.objects.all() # not adding context here
    context_object_name = "sectors"
    paginate_by = 2
    
class SectorsDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "industries/sector_detail.html"
    queryset = Sectors.objects.all() # not adding context here
    context_object_name = "sectors"
    
class SectorsCreateView(LoginRequiredMixin, CreateView):
    template_name = "industries/sector_create.html"
class SectorListView(LoginRequiredMixin, generic.ListView):
    template_name = "industries/sector_list.html"
    queryset = Sectors.objects.all() # not adding context here
    context_object_name = "sectors"
    paginate_by = 2
    
class SectorsDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "industries/sector_detail.html"
    queryset = Sectors.objects.all() # not adding context here
    context_object_name = "sectors"
    
class SectorsCreateView(LoginRequiredMixin, CreateView):
    template_name = "industries/sector_create.html"
    form_class = SectorsForm
    
    def get_success_url(self):
        return reverse("industries:sector-list")

class SectorsUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "industries/sector_update.html"
    form_class = SectorsForm
    queryset = Sectors.objects.all()
    
    def get_success_url(self):
        return reverse("industries:sector-list")
    
    
    def form_valid(self, form):
        form.save()
        messages.info(self.request, "You have successfully updated this lead")
        return super(SectorsUpdateView, self).form_valid(form)
    
class SectorsDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "industries/sector_delete.html"
    queryset = Sectors.objects.all()
    
    def get_success_url(self):
        return reverse("industries:sectors-list")


class SearchSectorView(ListView):
    model = Sectors
    template_name = "industries/sector_search.html"
    paginate_by= 1

    def get_queryset(self):  # new
        query = self.request.GET.get("q")
        object_list = Sectors.objects.filter(
            Q(industry__icontains=query)|
           Q(name__icontains=query)|
           Q(created_on__icontains=query)
            
            )
        return object_list
        #return reverse( "enterprises: enterprise-update")

@login_required
def Sectors_update(request, pk):
    sectors = Sectors.objects.get(id=pk)
    form = SectorsForm(instance=Sectors)
    if request.method == "POST":
        form = SectorsForm(request.POST, instance=Sectors)
        if form.is_valid():
            form.save()
            return redirect("industries:Sectors-list")
    context = {
        "form": form,
        "sectors": sectors
    }
    return render(request, "industries/sector_update.html", context)         


def detail(request, Sectors_id):
    try:
        Sectors = Sectors.objects.get(pk=Sectors_id)
    except Sectors.DoesNotExist:
        raise Http404("Sectors does not exist does not exist")
    return render(request, 'industries/sector_detail.html', {'sectors': Sectors})
    form_class = SectorsForm
    
    def get_success_url(self):
        return reverse("industries:sector-list")

class SectorsUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "industries/sector_update.html"
    form_class = SectorsForm
    queryset = Sectors.objects.all()
    
    def get_success_url(self):
        return reverse("industries:sector-list")
    
    
    def form_valid(self, form):
        form.save()
        messages.info(self.request, "You have successfully updated this lead")
        return super(SectorsUpdateView, self).form_valid(form)
    
class SectorsDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "industries/sector_delete.html"
    queryset = Sectors.objects.all()
    
    def get_success_url(self):
        return reverse("industries:sector-list")


class SearchSectorView(ListView):
    model = Sectors
    template_name = "industries/sector_search.html"
    paginate_by= 1

    def get_queryset(self):  # new
        query = self.request.GET.get("q")
        object_list = Sectors.objects.filter(
            Q(industry__icontains=query)|
           Q(name__icontains=query)|
           Q(created_on__icontains=query)
            
            )
        return object_list
        #return reverse( "enterprises: enterprise-update")
'''
@login_required
def Sectors_update(request, pk):
    sectors = Sectors.objects.get(id=pk)
    form = SectorsForm(instance=Sectors)
    if request.method == "POST":
        form = SectorsForm(request.POST, instance=Sectors)
        if form.is_valid():
            form.save()
            return redirect("industries:Sectors-list")
    context = {
        "form": form,
        "sectors": sectors
    }
    return render(request, "industries/sector_update.html", context)         


def detail(request, Sectors_id):
    try:
        Sectors = Sectors.objects.get(pk=Sectors_id)
    except Sectors.DoesNotExist:
        raise Http404("Sectors does not exist does not exist")
    return render(request, 'industries/sector_detail.html', {'sectors': Sectors})
'''
def sector_list(request):
    context = {'form': SectorsForm(), 'sectors': Sectors.objects.all()}
    return render(request, "industries/sector_list.html", context)
    
    
    
def sector_create(request):
    if request.method=="POST":
        form = SectorsForm(request.POST or None)
        if form.is_valid():
            sector = form.save()
            context = {'sector': sector}
            return render(request, 'industries/partials/sector.html', context)
    
    return render(request, "industries/partials/sector_create.html", {'form':SectorsForm })