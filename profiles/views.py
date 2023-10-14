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



def profile_page(request):
    expert_profile = ExpertProfile.objects.all()
    company_profile = CompanyProfile.objects.all()
    admin_profile = AdminProfile.objects.all()
    employee_profile = EmployeeProfile.objects.all()
    
    return render (request, 'profiles/profile_home.html',{"expert_profile": expert_profile, "company_profile": company_profile, 
                                                   "admin_profile": admin_profile, "employee_profile": employee_profile}) 
    
       
@login_required
def expert_profile_view(request):
    ex_profile = ExpertProfile.objects.get(user=request.user)
    form = ExpertProfileForm(request.POST or None, request.FILES or None)
    confirm = False

    if form.is_valid():
        form.save()
        confirm = True

    context = {
        'ex_profile': ex_profile,
        'form': form,
        'confirm': confirm,
    }
    return render(request, 'profiles/expert_profile.html', context)

@login_required
def company_profile_view(request):
    c_profile = CompanyProfile.objects.get(user=request.user)
    form = CompanyProfileForm(request.POST or None, request.FILES or None)
    confirm = False

    if form.is_valid():
        form.save()
        confirm = True

    context = {
        'c_profile': c_profile,
        'form': form,
        'confirm': confirm,
    }
    return render(request, 'profiles/company_profile.html', context)




@login_required
def employee_profile_view(request):
    profile = EmployeeProfile.objects.get(user=request.user)
    form = EmployeeProfileForm(request.POST or None, request.FILES or None)
    confirm = False

    if form.is_valid():
        form.save()
        confirm = True
    context = {
        'profile': profile,
        'form': form,
        'confirm': confirm,
    }
    return render(request, 'profiles/employee_profile.html', context)

@login_required
def admin_profile_view(request):
    profile = AdminProfile.objects.get(user=request.user)
    form = AdminProfileForm(request.POST or None, request.FILES or None)
    confirm = False

    if form.is_valid():
        form.save()
        confirm = True

    context = {
        'profile': profile,
        'form': form,
        'confirm': confirm,
    }
    return render(request, 'profiles/admin_profile.html', context)


@login_required
def my_profile_view(request):
    profile = ExpertProfile.objects.get(user=request.user)
    form = ExpertProfileForm(request.POST or None, request.FILES or None)
    confirm = False

    if form.is_valid():
        form.save()
        confirm = True

    context = {
        'profile': profile,
        'form': form,
        'confirm': confirm,
    }
    return render(request, 'profiles/expert_profile.html', context)