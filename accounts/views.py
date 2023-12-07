from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render
from django.shortcuts import render
from numpy import integer
from core.models import User
from .forms import UserCreateForm
from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.views.generic import (
    TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy
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

def testing(request):
    return render(request, 'accounts/testing.html')

class HomePageView(ListView):
    context_object_name = "data"
    template_name = "accounts/home_page.html"

    def get_queryset(self):
        my_set = {
            "deals": Deals.objects.all()[:2],
            "products": ProductDeals.objects.all()[:2],
            "blogs": Blog.objects.all()[:2],
            "experts": ExpertProfile.objects.all()[:2],
            "fiches": FicheTechnic.objects.all()[:2],
            "companies":Enterprises.objects.all()[:2],
            "jobs":Jobs.objects.all()[:2],
            "trainings": Trainings.objects.all()[:2],
            "experts_count": ExpertProfile.objects.count(),
            "experts_count": CustomUser.objects.filter(is_expert=True).count(),
            "companies_count": Enterprises.objects.count(),
            "deals_count": Deals.objects.count(),
            "product_deals_count": ProductDeals.objects.count(),
        }
        return my_set

def home_page(request):
    deals = Deals.objects.all()[:2]
    product_deals = ProductDeals.objects.all()[:2]
    blogs = Blog.objects.all()[:2]
    experts = ExpertProfile.objects.all()[:2]
    fiches = FicheTechnic.objects.all()[:2]
    companies = Enterprises.objects.all()[:2]
    jobs = Jobs.objects.all()[:2]
    trainings = Trainings.objects.all()[:2]
    #experts_count = ExpertProfile.objects.count()
    experts_count= CustomUser.objects.filter(is_expert=True).count()
    companies_count= Enterprises.objects.count()
    deals_count= Deals.objects.count()
    product_deals_count= ProductDeals.objects.count()
    return render (request, 'accounts/home_page.html',{"deals": deals, "blogs": blogs, #"experts": experts, 
                                                       "fiches": fiches, "companies":companies, "jobs": jobs, "trainings": trainings, "experts": experts,"experts_count": experts_count, "companies_count": companies_count, "deals_count": deals_count, "product_deals_count": product_deals_count, "product_deals": product_deals}) 
    
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
'''
class home_expert( generic.ListView):
    template_name = "accounts/home_expert.html"
    queryset = Experts.objects.all() # not adding context here
    context_object_name = "experts"
    paginate_by = 5
'''
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
            user = form.save()# old line of code just remove the comment to activate it
            #user = form.save(commit=False) #new line
            #user.is_active=False # new line
            #user.save() #new line
            first_name = user.first_name # old line of code just remove the comment to activate it
            last_name = user.last_name # old line of code just remove the comment to activate it
            name = first_name + ' ' + last_name # old line of code just remove the comment to activate it
            #UserProfile.objects.create(name=name, user=user)
            login(request, user) # old line of code just remove the comment to activate it
            #return redirect('accounts:home-page') 
            #activateEmail(request, user, form.cleaned_data.get('email')) # new line
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
            
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating form'
    return render(request, 'accounts/login.html', {'form': form, 'msg': msg})

def stats(request):
    deals_count = Deals.objects.count()
    
    return render(request, 'accounts/stats.html', {'deals_counts': deals_count})

### User Work experience ###

class WorkExperienceListView(ListView):
    model = WorkExperience
    template_name = 'accounts/work_experience_list.html'
    context_object_name = 'work_experiences'
    
    
class WorkExperienceCreateView( LoginRequiredMixin, CreateView):
    model = WorkExperience
    template_name = "accounts/work_experience_create.html"
    fields = ['company_name', 'position', 'work_location_address', 'work_city', 'work_country', 'job_title',
          'start_date', 'end_date', 'description']
    success_url = reverse_lazy('accounts:experience-list')
     
    def form_valid(self, form):
        form.instance.email = self.request.user.email
        form.instance.user = self.request.user
        #form.instance.user = CustomUser.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)
    
class ExpertPortfolioListView(ListView):
    model = ExpertPortfolio
    template_name = 'accounts/expert_portfolio_list.html'
    context_object_name = 'expert_portfolios'
    
class ExpertPortfolioCreateView( LoginRequiredMixin, CreateView):
    model = ExpertPortfolio
    template_name = "accounts/expert_portfolio_create.html"
    fields = ['project_title', 'project_type', 'client_name', 'technologies_used', "project_city", "project_country",
          'reference_email', 'start_date', 'end_date','description',]
    success_url = reverse_lazy('accounts:portfolio-list')
     
    def form_valid(self, form):
        form.instance.consultant_email = self.request.user.email
        form.instance.consultant = self.request.user
        #form.instance.user = CustomUser.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

class EducationListView(ListView):
    model = Education
    template_name = 'accounts/education_list.html'
    context_object_name = 'education'
    
class EducationCreateView( LoginRequiredMixin, CreateView):
    model = Education
    template_name = "accounts/education_create.html"
    fields = ["institution_name", "degree", "specialization", "minor", "start_date", "end_date","gpa","graduated", "description" ] 
    success_url = reverse_lazy('accounts:education-list')
     
    def form_valid(self, form):
        form.instance.student_email = self.request.user.email
        form.instance.student = self.request.user
        
        return super().form_valid(form) 


