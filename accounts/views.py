from django.contrib.auth import login, logout, authenticate, get_user_model
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
from django.http import HttpResponse  
from django.urls import reverse_lazy
from core.models import *
from core.forms import *
from .forms import *
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

# Add below existing imports
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language, activate, gettext
from django.utils import translation
from .tokens import account_activation_token, generate_confirmation_token

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
    
'''
def translate(language):
    cur_language = get_language()
    try:
        activate(language)
        text = gettext('hello')
    finally:
        activate(cur_language)
    return text
'''

def aboutus(request):
    #trans = translate(language='fr')
    #return render(request, 'accounts/aboutus.html', {'trans': trans})
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
def SignUp1(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            #user = form.save()# old line of code just remove the comment to activate it
            user = form.save(commit=False) #new line
            #user.is_active=False # new line
            #user.save() #new line
            first_name = user.first_name # old line of code just remove the comment to activate it
            last_name = user.last_name # old line of code just remove the comment to activate it
            name = first_name + ' ' + last_name # old line of code just remove the comment to activate it
            user.is_expert = True
            user.save()
            #UserProfile.objects.create(name=name, user=user)
            login(request, user) # old line of code just remove the comment to activate it
            #return redirect('accounts:home-page') 
            #activateEmail(request, user, form.cleaned_data.get('email')) # new line
            return redirect('accounts:home-page')
    else:
        form = UserCreateForm()
    return render(request, 'accounts/signup.html', {'form': form})

def SignUp_v1(request):
    if request.method == 'POST':
        next = request.GET.get('next')
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            first_name = user.first_name # old line of code just remove the comment to activate it
            last_name = user.last_name # old line of code just remove the comment to activate it
            name = first_name + ' ' + last_name # old line of code just remove the comment to activate it
            user.is_expert = True
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            #new_user = authenticate(email=user.email, password=password)
            new_user = authenticate(username=user.username, password=password)
            login(request, new_user)
            if next:
                return redirect(next)
            else:
                return redirect('accounts:verify-email')
    else:
        form = UserCreateForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/signup.html', context)

def SignUp(request):
    if request.method == 'POST':
        next = request.GET.get('next')
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            first_name = user.first_name # old line of code just remove the comment to activate it
            last_name = user.last_name # old line of code just remove the comment to activate it
            name = first_name + ' ' + last_name # old line of code just remove the comment to activate it
            user.is_expert = True
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            #new_user = authenticate(email=user.email, password=password)
            new_user = authenticate(username=user.username, password=password, )
            if not request.user.is_authenticated:
                return redirect('accounts:verify-email')
            else:
                login(request, new_user)
                if next:
                    return redirect(next)
                else:
                    return redirect('accounts:home-page')
    else:
        form = UserCreateForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/signup.html', context)


def signup(request):  
    if request.method == 'POST':  
        form = UserCreateForm(request.POST)  
        if form.is_valid():  
            # save form in the memory not in database  
            user = form.save(commit=False)  
            user.is_active = False  
            user.save()  
            # to get the domain of the current site  
            current_site = get_current_site(request)  
            mail_subject = 'Activation link has been sent to your email id'  
            message = render_to_string('accounts/acc_active_email.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':account_activation_token.make_token(user),  
            })  
            to_email = form.cleaned_data.get('email')  
            email = EmailMessage(  
                        mail_subject, message, to=[to_email]  
            )  
            email.send()  
            return HttpResponse('Please confirm your email address to complete the registration')  
    else:  
        form = UserCreateForm()  
    return render(request, 'accounts/signup.html', {'form': form})  

def activate1(request, uidb64, token):  
    #User = get_user_model()
    User = CustomUser  
    try:  
        uid = force_text(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        #return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        return redirect('accounts:home-page')  
    else:  
        return HttpResponse('Activation link is invalid!')  

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

class WorkExperienceUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "accounts/expert_experience_update.html"
    form_class = WorkExperienceForm
    queryset = WorkExperience.objects.all()
    
    def get_success_url(self):
        return reverse("profiles:expert-profile-list")
     
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

class ExpertPortfolioUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "accounts/expert_portfolio_update.html"
    form_class = ProjectPortfolioForm
    queryset = ExpertPortfolio.objects.all()
    
    def get_success_url(self):
        return reverse("profiles:expert-profile-list")
    
class EducationListView(ListView):
    model = Education
    template_name = 'accounts/education_list.html'
    context_object_name = 'education'
    
class EducationCreateView( LoginRequiredMixin, CreateView):
    model = Education
    template_name = "accounts/education_create.html"
    fields = ["institution_name", "degree", "specialization", "minor", "start_date", "end_date","gpa","graduated", "description" ] 
    success_url = reverse_lazy('profiles:expert-user-profile-list')
     
    def form_valid(self, form):
        form.instance.student_email = self.request.user.email
        form.instance.student = self.request.user
        
        return super().form_valid(form) 

class EducationUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "accounts/education_update.html"
    form_class = EducationModelForm
    queryset = Education.objects.all()
    
    def get_success_url(self):
        return reverse("profiles:expert-profile-list")
    
def logout_view(request):
    logout(request)
    return redirect('accounts/login.html')
 
def AdminSignUp(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            #user = form.save()# old line of code just remove the comment to activate it
            user = form.save(commit=False) #new line
            #user.is_active=False # new line
            #user.save() #new line
            first_name = user.first_name # old line of code just remove the comment to activate it
            last_name = user.last_name # old line of code just remove the comment to activate it
            name = first_name + ' ' + last_name # old line of code just remove the comment to activate it
            user.is_admin = True
            user.is_active = False
            user.save()
            #UserProfile.objects.create(name=name, user=user)
            login(request, user) # old line of code just remove the comment to activate it
            #return redirect('accounts:home-page') 
            #activateEmail(request, user, form.cleaned_data.get('email')) # new line
            return redirect('accounts:home-page')
    else:
        form = UserCreateForm()
    return render(request, 'accounts/admin_signup.html', {'form': form})


def EmployeeSignUp(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            #user = form.save()# old line of code just remove the comment to activate it
            user = form.save(commit=False) #new line
            #user.is_active=False # new line
            #user.save() #new line
            first_name = user.first_name # old line of code just remove the comment to activate it
            last_name = user.last_name # old line of code just remove the comment to activate it
            name = first_name + ' ' + last_name # old line of code just remove the comment to activate it
            user.is_employee = True
            user.is_active = False
            user.save()
            #UserProfile.objects.create(name=name, user=user)
            login(request, user) # old line of code just remove the comment to activate it
            #return redirect('accounts:home-page') 
            #activateEmail(request, user, form.cleaned_data.get('email')) # new line
            return redirect('accounts:home-page')
    else:
        form = UserCreateForm()
    return render(request, 'accounts/employee_signup.html', {'form': form})


class ReadContentView(ListView):
    context_object_name = "data"
    template_name = "accounts/read_content.html"

    def get_queryset(self):
        message_all = {
            "forms_read": FicheRead.objects.all(),
            "blogs_read": BlogRead.objects.all(),
            "deals_read": DealRead.objects.all(),
            "product_deals_read": ProductDealRead.objects.all(),
            
             }
        return message_all


# send email with verification link
def verify_email(request):
    if request.method == "POST":
        if request.user.email_is_verified != True:
        #if request.user.is_active != True:
            current_site = get_current_site(request)
            user = request.user
            #print(user.email_verified)
            #email = request.user.email
            subject = "Verify Email"
            message = render_to_string('accounts/verify_email_message.html', {
                'request': request,
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.id)),
                'token':account_activation_token.make_token(user),
                #'protocol': 'https' if request.secure() else 'http'
            })
            #email = form.cleaned_data.get('email')  
            email = EmailMessage(
                subject, message, to=[email]
            )
            email.content_subtype = 'html'
            email.send()
            return redirect('accounts:verify-email-done')
        else:
            return redirect('accounts:signup')
    return render(request, 'accounts/verify_email.html')


def verify_email_done(request):
    return render(request, 'accounts/verify_email_done.html')


def verify_email_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.email_is_verified = True
        user.is_active = True
        user.save()
        messages.success(request, 'Your email has been verified.')
        return redirect('accounts:verify-email-complete')   
    else:
        messages.warning(request, 'The link is invalid.')
    return render(request, 'accounts/verify_email_confirm.html')


def verify_email_complete(request):
    return render(request, 'accounts/verify_email_complete.html')

#### Registrations Email Confirmation method ###
#@user_not_authenticated
def initial_registration(request):
    return render(request, 'accounts/initial_registration.html')

def register(request):
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_expert = True
            user.is_active = False
            user.email_is_verified = False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('accounts:verify-email')

        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    else:
        form = UserCreateForm()

    return render(
        request=request,
        template_name="accounts/signup.html",
        context={"form": form}
        )

def activateEmail(request, user, to_email):
    mail_subject = 'Activate your user account.'
    message = render_to_string('accounts/template_activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
            received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_expert = True
        user.is_active = True
        user.email_is_verified = True
        user.save()

        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('accounts:login')
    else:
        messages.error(request, 'Activation link is invalid!')
    
    return redirect('accounts:home-page')
