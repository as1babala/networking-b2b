from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render
from django.shortcuts import render
from numpy import integer
from .models import User
from .forms import UserCreateForm
from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.views.generic import (
    TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
)
from core.models import *
from core.forms import *
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
def activateEmail(request, user, to_email):
    messages.success(request, f'Dear<b>{user}</b> please go to your email <b>{to_email}</b> inbox and click on\
    received activation link to confirm and complete the registration. <b>Note: </b> check your spam folder.')

def home(request):
    return render(request, 'accounts/home.html')


def home_page(request):
    deals = Deals.objects.all()
    blogs = Blog.objects.all()
    experts = Experts.objects.all()
    fiches = FicheTechnic.objects.all()
    companies = Enterprises.objects.all()
    jobs = Jobs.objects.all()
    trainings = Trainings.objects.all()
    return render (request, 'accounts/home_page.html',{"deals": deals, "blogs": blogs, "experts": experts, 
                                                       "fiches": fiches, "companies":companies, "jobs": jobs, "trainings": trainings}) 


def aboutus(request):
    return render(request, 'accounts/aboutus.html')

def privacy(request):
    return render(request, 'accounts/privacy_policy.html')

def conditions(request):
    return render(request, 'accounts/terms_and_conditions.html')

def contact(request):
    return render(request, 'accounts/contact.html')

def services(request):
    return render(request, 'accounts/services.html')

def packages(request):
    return render(request, 'accounts/packages.html')

class home_business( generic.ListView):
    template_name = "accounts/home_business.html"
    #queryset = Opportunities.objects.all() # not adding context here
    #context_object_name = "opportunities"
    #paginate_by = 5

class home_expert( generic.ListView):
    template_name = "accounts/home_expert.html"
    queryset = Experts.objects.all() # not adding context here
    context_object_name = "experts"
    paginate_by = 5

class home_employee( generic.ListView):
    template_name = "accounts/home_employee.html"
    #queryset = Employees.objects.all() # not adding context here
    #context_object_name = "opportunities"
    #paginate_by = 5


class home_admin( generic.ListView):
    template_name = "accounts/home_admin.html"
    #queryset = Opportunities.objects.all() # not adding context here
    #context_object_name = "opportunities"
    #paginate_by = 5

### Signup views ####
def SignUp(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            first_name = user.first_name
            last_name = user.last_name
            name = first_name + ' ' + last_name
            #UserProfile.objects.create(name=name, user=user)
            login(request, user)
            return redirect('accounts:home-page')
    else:
        form = UserCreateForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    form = UserCreateForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_admin:
                login(request, user)
                return redirect('accounts:home-admin')
            elif user is not None and user.is_employee:
                login(request, user)
                return redirect('accounts:home-employee')
            elif user is not None and user.is_expert:
                login(request, user)
                return redirect('accounts:home-expert')
            elif user is not None and user.is_company:
                login(request, user)
                return redirect('accounts:home-company')
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating form'
    return render(request, 'accounts/login.html', {'form': form, 'msg': msg})
        

