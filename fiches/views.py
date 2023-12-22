from itertools import count
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.views.generic import (
    TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.decorators import login_required,user_passes_test
from django.db.models import Q
from django.http.response import HttpResponse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.core.mail import send_mail
#from slick_reporting.views import SlickReportView
#from slick_reporting.fields import SlickReportField
from core.models import FicheTechnic
from .forms import *
from django.db.models import Count

# Create your views here.

class admin(UserPassesTestMixin):
    
    def test_func(self):
        return self.request.user.is_admin
    
class employee(UserPassesTestMixin):
    
    def test_func(self):
        return self.request.user.is_employee
class FicheTechnicListView(LoginRequiredMixin, generic.ListView):
    template_name = "fiches/fiche_list.html"
    queryset = FicheTechnic.objects.all() # not adding context here
    context_object_name = "fiches"
    paginate_by = 2
    
class FicheTechnicDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "fiches/fiche_detail.html"
    queryset = FicheTechnic.objects.all() # not adding context here
    context_object_name = "fiches"
         
     
     

class FicheTechnicCreateView(admin, employee, CreateView):
    template_name = "fiches/fiche_create.html"
    form_class = FicheTechnicForm
    
    def get_success_url(self):
        return reverse("fiches:fiche-list")

class FicheTechnicUpdateView( admin, generic.UpdateView):
    template_name = "fiches/fiche_update.html"
    form_class = FicheTechnicForm
    queryset = FicheTechnic.objects.all()
    
    def get_success_url(self):
        return reverse("fiches:fiche-list")
    
    
    def form_valid(self, form):
        form.save()
        messages.info(self.request, "You have successfully updated this lead")
        return super(FicheTechnicUpdateView, self).form_valid(form)
    
class FicheTechnicDeleteView(admin, generic.DeleteView):
    template_name = "fiches/fiche_delete.html"
    queryset = FicheTechnic.objects.all()
    
    def get_success_url(self):
        return reverse("fiches:fiche-list")
#### PDF template
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
        return HttpResponse(result.getvalue(), content_type='fiches/fiche_pdf.html')
    return



def download_pdf_view(request,pk):
    fichesDetail=FicheTechnic.objects.all().filter(id=pk).order_by('-id')[:1]
    dict={
        'User':fichesDetail[0].user,
        'dob':fichesDetail[0].DOB,
        'EmpTitle':fichesDetail[0].emp_title, 
        'Country':fichesDetail[0].country, 
        'email':fichesDetail[0].email,
        'bio':fichesDetail[0].bio,  
    }
    return render_to_pdf('fiches/fiche_pdf.html',dict)

##### Search Function

class FicheTechnicSearchView(ListView):
    model = FicheTechnic
    template_name = "fiches/fiche_search.html"
    paginate_by= 1

    def get_queryset(self):  # new
        query = self.request.GET.get("q")
        object_list = FicheTechnic.objects.filter(
            Q(name__icontains=query) | 
            Q(category__icontains=query)  |
            Q(principal_risks__icontains=query)  
            
            
           
            )
        return object_list
# Create your views here.

def fiche_detail(request, slug):
    fiches = FicheTechnic.objects.get(slug=slug)
    ### Creating the deal viewing history
    user = request.user
    if not FicheRead.objects.filter(reader=user, fiche_read=fiches).exists():
        FicheRead.objects.create(reader=user, fiche_read=fiches)
    
    context ={
        "fiches": fiches,
    }
        
    return render(request, "fiches/fiche_detail.html", context)

def fiche_read_history(request):
    # Assuming you have the user object available
    return render(request, 'fiches/fiche_read_history.html', {'reader': request.user})