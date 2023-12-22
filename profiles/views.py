from itertools import count
from typing import Any
from django.db.models.query import QuerySet
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

class ExpertProfileListView(LoginRequiredMixin, generic.ListView):
    template_name = "profiles/expert_list.html"
    queryset = ExpertProfile.objects.all() # not adding context here
    context_object_name = "expert_profiles"
    paginate_by = 8
    
class ExpertProfileListView(LoginRequiredMixin, generic.ListView):
    template_name = "profiles/expert_list.html"
    queryset = ExpertProfile.objects.all() # not adding context here
    context_object_name = "expert_profiles"
    paginate_by = 8
     
@login_required
def view_profile(request):
    
    profile = ExpertProfile.objects.get(email=request.user.email)
    #profile = ExpertProfileForm(request.POST or None, request.FILES or None)
    form = ExpertProfileForm(request.POST or None, request.FILES or None)
    return render(request, 'profiles/expert_profile.html', {'profile': profile})

class ExpertProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "profiles/expert_update.html"
    form_class = ExpertProfileForm
    queryset = ExpertProfile.objects.all()
    
    
    def get_success_url(self):
        return reverse("profiles:expert-user-profile-list")
     
    def form_valid(self, form):
        form.save()
        messages.info(self.request, "You have successfully updated this lead")
        return super(ExpertProfileUpdateView, self).form_valid(form)
    

class ExpertProfileDetailView1(LoginRequiredMixin, generic.DetailView):
    template_name = "profiles/expert_detail.html"
    queryset = ExpertProfile.objects.all() # not adding context here
    context_object_name = "profiles"

class ExpertProfileDetailView(LoginRequiredMixin, generic.DetailView):
    model = ExpertProfile
    template_name = 'profiles/expert_detail.html'
    context_object_name = 'profiles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['profiles'] = ExpertProfile.objects.get(user=self.object.user)
        context['education'] = Education.objects.filter(student=self.object.user)
        context['work_experience'] = WorkExperience.objects.filter(user=self.object.user)
        context['expert_portfolio'] = ExpertPortfolio.objects.filter(consultant=self.object.user)
        return context
    
class ExpertProfileDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "profiles/expert_delete.html"
    queryset = ExpertProfile.objects.all()
    
    def get_success_url(self):
        return reverse("profiles:expert-profile-list")

class ExpertMessagingCreateView( LoginRequiredMixin, CreateView):
    model = ExpertMessaging
    fields = [ 'subject', 'content', 'attached_file']
    template_name = "profiles/expert_message_create.html"
    success_url = reverse_lazy('profiles:expert-profile-list')
     
    def form_valid(self, form):
        form.instance.sender_name = self.request.user
        form.instance.sender_email = self.request.user.email
        form.instance.expert = ExpertProfile.objects.get(pk=self.kwargs['expert_id'])
        #form.instance.expert = ExpertProfile.objects.get(user=self.request.user)
        return super().form_valid(form)

def send_message1(request, expert_id):
    expert = get_object_or_404(ExpertProfile, id=expert_id)
    form = MessageForm(request.POST or None)

    if request.method == 'POST':
        def form_valid(self, form):
            form.instance.sender_name = self.request.user
            form.instance.sender_email = self.request.user.email
            form.instance.expert = get_object_or_404(ExpertProfile, id=expert_id)
            #form.instance.expert = ExpertProfile.objects.get(user=self.request.user)
            return redirect('profiles:expert-profile-list')

    return render(request, 'profiles/expert_message_create.html', {'form': form, 'expert': expert})

def send_message( request, expert_id):
    expert = get_object_or_404(ExpertProfile, id=expert_id)
    form = MessageForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            message = form.save(commit=False)
            message.sender= request.user
            message.sender_email = request.user.email
            #message.sender = request.user
            message.expert = expert
            message.save()
            return redirect('profiles:expert-profile-list')

    return render(request, 'profiles/expert_message_create.html', {'form': form, 'expert': expert})

class ExpertMessageListView(LoginRequiredMixin, generic.ListView):
    template_name = "profiles/expert_message_list.html"
    queryset = ExpertMessaging.objects.all() # not adding context here
    context_object_name = "expert_message"
    paginate_by = 8


class ExpertMessageReceivedListView(LoginRequiredMixin, generic.ListView):
    template_name = "profiles/expert_received_message_list.html"
     # not adding context here
    context_object_name = "expert_received_message"
    paginate_by = 8
    
    def get_queryset(self):
        return ExpertMessaging.objects.filter(expert=self.request.user)

class ExpertMessageSentListView(LoginRequiredMixin, generic.ListView):
    template_name = "profiles/expert_sent_message_list.html"
     # not adding context here
    context_object_name = "expert_sent_message"
    paginate_by = 8
    
    def get_queryset(self):
        return ExpertMessaging.objects.filter(sender=self.request.user)



def profile_(request):
    expert_profile = ExpertProfile.objects.all()
    admin_profile = AdminProfile.objects.all()
    employee_profile = EmployeeProfile.objects.all()
    
    return render (request, 'profiles/profile_home.html',{"expert_profile": expert_profile, 
                                                   "admin_profile": admin_profile, "employee_profile": employee_profile}) 
    
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

def userpage(request):
	user_form = ExpertProfile(instance=request.user)
	profile_form = ExpertProfileForm(instance=request.user.profile)
	return render(request=request, template_name="profiles/expert_profile.html", context={"user":request.user, "user_form":user_form, "profile_form":profile_form })


class ExpertProfileSearchView(ListView):
    model = ExpertProfile
    template_name = "profiles/expert_profile_search.html"

    def get_queryset(self):  # new
        query = self.request.GET.get("q")
        object_list = ExpertProfile.objects.filter(
            
            Q(user__icontains=query)| 
            Q(email__icontains=query)|
            Q(city__icontains=query)|
            Q(state__icontains=query)|
            Q(country__icontains=query)|
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)|
            Q(company_name__icontains=query)
        )
        return object_list   
 

class ExpertUserProfileListView(LoginRequiredMixin, generic.ListView):
    template_name = "profiles/expert_profile_user_list.html"
    context_object_name = "user_profiles"
    
    def get_queryset(self):
        return ExpertProfile.objects.filter(user=self.request.user)
    
class AdminProfileListView(LoginRequiredMixin, generic.ListView):
    template_name = "profiles/admin_list.html"
    queryset = AdminProfile.objects.all() # not adding context here
    context_object_name = "admin_profiles"
    paginate_by = 8


   