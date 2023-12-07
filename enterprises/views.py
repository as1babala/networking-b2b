from itertools import count
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.views.generic import (
    TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
#from slick_reporting.views import SlickReportView
#from slick_reporting.fields import SlickReportField
from core.models import *
from .forms import *
from django.db.models import Count
from django.http import JsonResponse
from industries.forms import *
from .filters import EnterprisesFilter

class EnterpriseListView1(LoginRequiredMixin, generic.ListView):
    model = Enterprises
    template_name = "enterprises/enterprise_list.html"
    queryset = Enterprises.objects.all() # not adding context here
    context_object_name = "enterprises"
    paginate_by = 3
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = EnterprisesFilter(self.request.GET, queryset=self.get_queryset())
        #context['filter'] = self.ProjectFilter(self.request.GET, queryset=self.get_queryset())
        return context

class EnterpriseListView(LoginRequiredMixin, generic.ListView):
    model = Enterprises
    template_name = "enterprises/enterprise_list.html"
    queryset = Enterprises.objects.all() # not adding context here
    context_object_name = "enterprises"
    paginate_by = 3
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = EnterprisesFilter(self.request.GET, queryset=self.get_queryset())
        #context['filter'] = self.ProjectFilter(self.request.GET, queryset=self.get_queryset())
        return context

class EnterpriseListView2(LoginRequiredMixin, generic.ListView):
    model = Enterprises
    template_name = "enterprises/enterprise_list.html"
    queryset = Enterprises.objects.all() # not adding context here
    context_object_name = "enterprises"
    paginate_by = 3
    
       
class EnterpriseDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "enterprises/enterprise_detail.html"
    queryset = Enterprises.objects.all() # not adding context here
    context_object_name = "enterprises"
    
class EnterpriseCreateView(LoginRequiredMixin, CreateView):
    template_name = "enterprises/enterprise_create.html"
    model = Enterprises
    form_class = EnterprisesForm
    
    def get_success_url(self):
        return reverse("enterprises:enterprise-list")
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, f'Your account has been created! You are now able to log in')
            
        return super().form_valid(form)

def load_industry(request):
    industry_id = request.GET.get('industry')
    sectors = Sectors.objects.filter(industry_id=industry_id).order_by('name')
    return render(request, 'enterprises/sectors_dropdown_list_options.html', {'sectors': sectors} )





def get_json_industry_data(request):
    qs_industry = list(Industry.objects.all())
    return JsonResponse({'qs_industry': qs_industry})




def companies(request):
    form = EnterprisesForm()
    if request.method == "POST":
        form = EnterprisesForm(request.POST)   
        if form.is_valid():
            enterprise = form.save(commit=False)
        
    
    return render(request, "enterprises/enterprise_create.html", {"form":form})

class EnterpriseUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "enterprises/enterprise_update.html"
    form_class = EnterprisesForm
    queryset = Enterprises.objects.all()
    
    def get_success_url(self):
        return reverse("enterprises:enterprise-list") 
    
    def form_valid(self, form):
        form.save()
        messages.info(self.request, "You have successfully updated this lead")
        return super(EnterpriseUpdateView, self).form_valid(form)
    
class EnterpriseDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "enterprises/enterprise_delete.html"
    queryset = Enterprises.objects.all()
    
    def get_success_url(self):
        return reverse("enterprises:enterprise-list")


class SearchEntView(ListView):
    model = Enterprises
    template_name = "enterprises/enterprise_search.html"
    paginate_by= 1

    def get_queryset(self):  # new
        query = self.request.GET.get("q")
        object_list = Enterprises.objects.filter(
            Q(company_name__icontains=query) | 
            Q(company_email__icontains=query)  |
            Q(company_address__icontains=query)  |
            Q(company_city__icontains=query)|
            Q(company_country__icontains=query)| 
            Q(company_type__icontains=query)|
            Q(commercial__icontains=query)|
            Q(technical__icontains=query)|
            Q(financial__icontains=query)|
            Q(management__icontains=query)|
            Q(company_web__icontains=query)|
            Q(sector__icontains=query)|
            Q(industry__icontains=query)|
            Q(annual_revenue__icontains=query)
            
            )
        return object_list
        #return reverse( "enterprises: enterprise-update")

                

@login_required
def CallSummary(request):
    qs = Enterprises.objects.values('enterprise').annotate(total_cnt=Count('id'))
    
    qs2 = Enterprises.objects.values('name').annotate(total_cnt=Count('name'))
    qs3 = Enterprises.objects.values('lead').annotate(total_cnt=Count('id'))
    qs4 = Enterprises.objects.values('name').annotate(total_cnt=Count('id'), unique= Count('name', distinct=True))
    context = {
        'qs': qs,
        'qs2': qs2,
        'qs3': qs3,
        'qs4': qs4
    }
    return render (request, "calls/call_report.html", context)
###### Jobs Area ###

def get_sectors(request, industry_id):
    sectors = Sectors.objects.filter(industry_id=industry_id).values('id', 'name')
    return JsonResponse(list(sectors), safe=False)
##### PDF ####
import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='enterprises/enterprise_pdf.html')
    return

def downloadCompany_pdf(request,pk):
    enterpriseDetail=Enterprises.objects.all().filter(id=pk).order_by('-id')[:1]
    dict={
        'User':enterpriseDetail[0].user,
        'dob':enterpriseDetail[0].DOB,
        'EmpTitle':enterpriseDetail[0].emp_title, 
        'Country':enterpriseDetail[0].country, 
        'email':enterpriseDetail[0].email,
        'bio':enterpriseDetail[0].bio,  
    }
    return render_to_pdf('enterprises/enterprise_pdf.html',dict)



