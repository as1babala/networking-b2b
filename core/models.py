from django.db import models
from django.shortcuts import reverse
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.dispatch import receiver
from common.utils import *
from django.utils.text import slugify
from accounts.models import CustomUser
from django.contrib.auth import get_user_model

from django.utils.translation import pgettext_lazy, gettext_lazy as _
from datetime import datetime
from django.conf import settings
from django.utils import timezone
from django_random_id_model import RandomIDModel
from django.dispatch import receiver
import stripe
from profiles.models import *
from ckeditor.fields import RichTextField
#from django_extensions.db.fields import RandomPrimaryKey
import shortuuid
from django.core.exceptions import ValidationError
#from phonenumber_field.modelfields import PhoneNumberField
import stripe
from tinymce import HTMLField
#stripe.api_key = settings.STRIPE_SECRET_KEY

#User = CustomUser
# Create your models here.

class Pricing(models.Model):
    name = models.CharField(_('pricing tier'), max_length=100) # free / basic / pro
    
    def __str__(self):
        return self.name
    

class Subscription(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    pricing = models.ForeignKey(Pricing, on_delete=models.CASCADE, related_name='subscriptions', null=True, blank=True)# query = Pricing.subcriptions.all()
    created = models.DateTimeField(auto_now_add=True)
    stripe_subscription_id = models.CharField(max_length=50, default="")
    status = models.CharField(max_length=100)
    
    def __str__(self):
        return self.user.email
    
### Adding stripe variables to the subscription app the subscription from stripe API   ####
def post_save_user(sender, instance, created, *args, **kwargs):
    if created:
        free_trial_pricing = Pricing.objects.get(name='Free Trial')
        subscription = Subscription.objects.create(user=instance, pricing=free_trial_pricing)
        stripe_customer = stripe.Customer.create( email=instance.email)
        stripe_subscription = stripe.Subscription.create(
            customer =stripe_customer["id"],
            item = [
                {'price': "price_1MnBxrFnCvJSP7I7637fsT3v"}
                ],
            trial_period_days = 7
            
        )
        print(stripe_subscription)
        subscription.status = stripe_subscription["status"]
        subscription.stripe_subscription_id = stripe_subscription["id"]
        subscription.save()
    
           
class Product(RandomIDModel):
    slug = models.SlugField(unique=True)
    product_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, default="")
    description = models.CharField(max_length=255, default="")
    product_features = models.CharField(max_length=255, default="")
    price = models.PositiveIntegerField(default=0) # cents 1000 = $10.00
    created_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.id
    
def pre_save_product(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.product_name)        
    


class Employee(RandomIDModel):
#class Employee(models.Model):
    slug = models.SlugField(unique=True)
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE, null=True, blank=True)
    user_type = models.OneToOneField(CustomUser, on_delete=models.CASCADE, default='EMPLOYEE', related_name='employees')
    DOB = models.DateField()
    prof_pic = models.ImageField(upload_to='employee_pictures/',null=True,blank=True)
    street_number = models.CharField(max_length=5, default="")
    city = models.CharField(max_length = 66, default="")
    state = models.CharField(default='', max_length = 2)
    country = models.CharField(choices=COUNTRIES, max_length =2, default="" )
    department = models.CharField(choices=DEPARTMENTS, max_length = 50, default="")
    emp_title = models.CharField(choices=EMP_TITLE, max_length = 3, default="")
    phone_code = models.CharField(max_length=10, choices=PHONE_CODE, default="")
    phone_number = models.CharField(max_length=10, default="")
    email = models.EmailField()
    sex = models.CharField(choices=SEX, max_length=1, default="")
    contract = models.CharField(choices=CONTRACT, max_length=2, default="")
    hired_date = models.DateField()
    #start_date = models.DateField(1/1/1900)
    is_employee = models.BooleanField('Is employee', default=True)
    year_since_hired =  models.PositiveIntegerField(null=True)
    bio = models.TextField(max_length=1000)
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField( auto_now=True) 
   
    class Meta: 
        verbose_name = "Employee"
        verbose_name_plural = "Employees"

    @property 
    def nbr_yr_exp(self):
        now = timezone.now().date()
        #diff = now - self.start_date
        nbr_yr_exp =  now - self.hired_date
        nbr_yr_exp_stripped = str(nbr_yr_exp).split(" ", 1)[0]
        nbr_exp = int(nbr_yr_exp_stripped)
        yrs_exp = round((nbr_exp/365)) 
        return yrs_exp
    
    @property 
    def emp_age(self):
        now = timezone.now().date()
        emp_age =  now - self.DOB
        emp_age_stripped = (str(emp_age).split(" ", 1)[0])
        nbr = int(emp_age_stripped)
        nbr_yrs = round((nbr/365),0)
       
        return nbr_yrs
    
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    
    @property
    def get_id(self):
        return self.id
    
    
    def get_absolute_url(self):
        return reverse("employees:employee-detail", kwargs={"slug": self.slug})
    
    def __str__(self):
        return self.email

##For pre_save; with this, the slug will not be created if already exist
def pre_save_employee(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.user)
''''
def post_save_employee(sender, instance, created, *args, **kwargs):
    if created:
        if instance.is_employee:
            Employee.objects.create(user=instance, last_name = instance.last_name, first_name = instance.first_name, 
                                    email = instance.email
            )             

'''

class Experts(RandomIDModel):
#class Experts(models.Model):
    slug = models.SlugField(unique=True)
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE, related_name='expert_users', default='')
    #user_type = models.OneToOneField(CustomUser, on_delete=models.CASCADE, default='EXPERT', related_name='experts')
    first_name = models.CharField(max_length=100, default="")
    last_name = models.CharField(max_length=100, default="")
    company_name = models.CharField(max_length=50, default="")
    DOB = models.DateField(null=True)
    prof_pic = models.ImageField(upload_to='document/', default='blog_pics/person_icon 1.png')
    street_number = models.CharField(max_length=5, default="", blank=True, null=True)
    city = models.CharField(max_length = 66, default="")
    state = models.CharField( max_length = 2, default="")
    country = models.CharField(choices=COUNTRIES, max_length =2, default="" )   
    phone_code = models.CharField(max_length=10, choices=PHONE_CODE, default="")
    phone_number = models.CharField(max_length=10, default="")
    email = models.EmailField()
    sex = models.CharField(choices=SEX, max_length=1)
    commercial = models.BooleanField('Would like to be a commercial partner', default=False)
    technical = models.BooleanField('Would like to be a technical partner', default=False)
    financial = models.BooleanField('Would like to be a financial partner', default=False)
    management = models.BooleanField('Would like to be a management partner', default=False)
    is_expert = models.BooleanField('Is Expert', default=True)
    bio = models.TextField(max_length=1000)
    #resume = models.FileField(upload_to='Expert_resumes/', default="")
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField( auto_now=True) 
   
    class Meta: 
        verbose_name = "Expert"
        verbose_name_plural = "Experts"
    
    @property 
    def consultant_age(self):
        now = timezone.now().date()
        consultant_age =  now - self.DOB
        consultant_age_stripped = (str(consultant_age).split(" ", 1)[0])
        nbr = int(consultant_age_stripped)
        nbr_yrs = round((nbr/365),0)
       
        return nbr_yrs
    
    @property
    def get_id(self):
        return self.id
    
    def get_absolute_url(self):
        return reverse("experts:expert-detail", kwargs={"slug": self.slug})
    
    def __str__(self):
        return self.user.email
 
def pre_save_expert(sender, instance, *args, **kwargs):
    if not instance.slug:
        #instance.slug = slugify(f"{instance.user}-{instance.id}")
        instance.slug = slugify(instance.id)
       
def post_save_expert(sender, instance, created, *args, **kwargs):
    if created:
        if instance.is_expert:
            Experts.objects.create(user=instance, last_name = instance.last_name, first_name = instance.first_name, 
                                    company_name = instance.company_name, email = instance.email, commercial=instance.commercial, technical=instance.technical,
                                    financial=instance.financial, management=instance.management
            )             


class AdminProfile(RandomIDModel):
    slug = models.SlugField(unique=True)
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, default="")
    last_name = models.CharField(max_length=100, default="")
    DOB = models.DateField(null=True)
    prof_pic = models.ImageField(upload_to='document/', default='blog_pics/person_icon 1.png')
    street_number = models.CharField(max_length=5, default="")
    city = models.CharField(max_length = 66, default="")
    state = models.CharField( max_length = 2, default="")
    country = models.CharField(choices=COUNTRIES, max_length =2, default="" )
    phone_code = models.CharField(max_length=10, choices=PHONE_CODE, default="")
    phone_number = models.CharField(max_length=10, default="")
    email = models.EmailField()
    sex = models.CharField(choices=SEX, max_length=1)
    is_consultant = models.BooleanField('Is Consultant', default=True)
    bio = models.TextField(max_length=1000)
    resume = models.FileField(upload_to='Expert_resumes/', default="")
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField( auto_now=True) 
   
    class Meta: 
        verbose_name = "Admin Profile"
        verbose_name_plural = "Admin Profiles"
    
    @property 
    def consultant_age(self):
        now = timezone.now().date()
        consultant_age =  now - self.DOB
        consultant_age_stripped = (str(consultant_age).split(" ", 1)[0])
        nbr = int(consultant_age_stripped)
        nbr_yrs = round((nbr/365),0)
       
        return nbr_yrs
    
    @property
    def get_name(self):
        return self.user
    
    
    def get_absolute_url(self):
        return reverse("accounts:admin-detail", kwargs={"slug": self.slug})
    
    @property
    def get_id(self):
        return self.id
    
    def __str__(self):
        return self.user.email

def pre_save_admin_p(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(f"{instance.user}-{instance.id}")
        
def post_save_admin_p(sender, instance, created, *args, **kwargs):
    if created:
        if instance.is_admin:
            AdminProfile.objects.create(user=instance, last_name = instance.last_name, first_name = instance.first_name, 
                                     email = instance.email
                                     )

class EmployeeProfile(RandomIDModel):
    slug = models.SlugField(unique=True)
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    DOB = models.DateField()
    prof_pic = models.ImageField(upload_to='employee_pictures/', default='blog_pics/person_icon 1.png')
    street_number = models.CharField(max_length=5, default="")
    city = models.CharField(max_length = 66, default="")
    state = models.CharField(default='', max_length = 2)
    country = models.CharField(choices=COUNTRIES, max_length =2, default="" )
    department = models.CharField(choices=DEPARTMENTS, max_length = 50, default="")
    emp_title = models.CharField(choices=EMP_TITLE, max_length = 3, default="")
    phone_code = models.CharField(max_length=10, choices=PHONE_CODE, default="")
    phone_number = models.CharField(max_length=10, default="")
    email = models.EmailField()
    sex = models.CharField(choices=SEX, max_length=1, default="")
    contract = models.CharField(choices=CONTRACT, max_length=2, default="")
    hired_date = models.DateField()
    #start_date = models.DateField(1/1/1900)
    is_employee = models.BooleanField('Is employee', default=False)
    year_since_hired =  models.PositiveIntegerField(null=True)
    bio = models.TextField(max_length=1000)
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField( auto_now=True) 
   
    class Meta: 
        verbose_name = "Employee Profile"
        verbose_name_plural = "Employee Profiles"

    @property 
    def nbr_yr_exp(self):
        now = timezone.now().date()
        #diff = now - self.start_date
        nbr_yr_exp =  now - self.hired_date
        nbr_yr_exp_stripped = str(nbr_yr_exp).split(" ", 1)[0]
        nbr_exp = int(nbr_yr_exp_stripped)
        yrs_exp = round((nbr_exp/365)) 
        return yrs_exp
    
    @property 
    def emp_age(self):
        now = timezone.now().date()
        emp_age =  now - self.DOB
        emp_age_stripped = (str(emp_age).split(" ", 1)[0])
        nbr = int(emp_age_stripped)
        nbr_yrs = round((nbr/365),0)
       
        return nbr_yrs
    
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    
    @property
    def get_id(self):
        return self.id
    
    def get_absolute_url(self):
        return reverse("employees:employee-detail", kwargs={"slug": self.slug})
    
    def __str__(self):
        return self.email
    
def pre_save_employee_p(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(f"{instance.user}-{instance.id}")
'''      
def post_save_employee_p(sender, instance, created, *args, **kwargs):
    if created:
        if instance.is_employee:
            EmployeeProfile.objects.create(user=instance, last_name = instance.last_name, first_name = instance.first_name, 
                                     email = instance.email
            )
'''
class ExpertProfile(RandomIDModel):
    slug = models.SlugField(unique=True)
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, default="")
    last_name = models.CharField(max_length=100, default="")
    DOB = models.DateField(null=True)
    company_name = models.CharField(max_length=50, null=True, blank=True)
    prof_pic = models.ImageField(upload_to='document/', default='blog_pics/person_icon 1.png')
    street_number = models.CharField(max_length=5, default="")
    city = models.CharField(max_length = 66, default="")
    state = models.CharField( max_length = 2, default="")
    country = models.CharField(choices=COUNTRIES, max_length =2, default="" )
    phone_code = models.CharField(max_length=10, choices=PHONE_CODE, default="")
    phone_number = models.CharField(max_length=10, default="")
    email = models.EmailField()
    sex = models.CharField(choices=SEX, max_length=1)
    is_expert = models.BooleanField('Is Expert', default=True)
    commercial = models.BooleanField('Would like to be a commercial partner', default=False)
    technical = models.BooleanField('Would like to be a technical partner', default=False)
    financial = models.BooleanField('Would like to be a financial partner', default=False)
    management = models.BooleanField('Would like to be a management partner', default=False)
    bio = models.TextField(max_length=1000)
    #resume = models.FileField(upload_to='Expert_resumes/', default="")
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField( auto_now=True) 
   
    class Meta: 
        verbose_name = "Expert Profile"
        verbose_name_plural = "Expert Profiles"
    
    @property 
    def consultant_age(self):
        now = timezone.now().date()
        consultant_age =  now - self.DOB
        consultant_age_stripped = (str(consultant_age).split(" ", 1)[0])
        nbr = int(consultant_age_stripped)
        nbr_yrs = round((nbr/365),0)
       
        return nbr_yrs
    
    @property
    def get_name(self):
        return self.user
    
    
    def get_absolute_url(self):
        return reverse("profiles:expert-detail", kwargs={"slug": self.slug})
    
    @property
    def get_id(self):
        return self.id
    
    def __str__(self):
        return self.user.email

def pre_save_expert_p(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(f"{instance.user}-{instance.id}")
        
def post_save_expert_p(sender, instance, created, *args, **kwargs):
    if created:
        if instance.is_expert:
            ExpertProfile.objects.create(user=instance, last_name = instance.last_name, first_name = instance.first_name, 
                                     company_name = instance.company_name, email = instance.email, commercial=instance.commercial, technical=instance.technical,
                                     financial=instance.financial, management=instance.management
                                     )

class Industry(models.Model):
    #industry_id = models.IntegerField(primary_key=True)
    name = models.CharField(choices=INDCHOICES, max_length=255, unique=True)
    description = models.TextField(max_length=255)
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now = True)
    
    class Meta:
        ordering = ('-created_on',)
        verbose_name = "Industry"
        verbose_name_plural = "Industries"
    
    def __str__(self):
        return self.name

class Sectors(models.Model):
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE, verbose_name='Industry')
    name = models.CharField(max_length=100, unique=True, default="", null=True)
    description = models.TextField(max_length=500)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    class Meta:
        
        ordering = ('-created_on',)
        verbose_name = "Sector"
        verbose_name_plural = "Sectors"
    
    def __str__(self):
        return self.name
    
class Enterprises(RandomIDModel):
#class Enterprises(models.Model):
    slug = models.SlugField(unique = True )
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, default="")
    last_name = models.CharField(max_length=100, default="")
    email = models.EmailField()
    registration_id = models.CharField(max_length=50, default="", null=True)
    registration_date = models.DateField(null=True)
    company_name = models.CharField(max_length=50)
    company_type = models.CharField(max_length=50, choices=TYPE_COMPANIES, default = '')
    company_email = models.EmailField()
    company_address = models.CharField(max_length=255)
    company_city = models.CharField(max_length=100)
    company_country = models.CharField(max_length=255, choices=COUNTRIES)
    industry = models.ForeignKey(Industry, on_delete=models.SET_NULL, null=True)
    sector = models.ForeignKey(Sectors, on_delete=models.SET_NULL, null=True)
    company_web = models.CharField(max_length=255)
    phone_code = models.CharField(max_length=10, choices=PHONE_CODE)
    phone_number = models.CharField(max_length=10)
    number_employees = models.CharField(max_length=15, choices=EMP_NUMBER, default='0_10')
    activity_description = models.TextField(max_length=500)
    annual_revenue = models.CharField(max_length = 50, choices=REVENUE, default='0_150 000 000')
    is_company = models.BooleanField('Would like to register my company', default=False)
    commercial = models.BooleanField('Would like to be a commercial partner', default=False)
    technical = models.BooleanField('Would like to be a technical partner', default=False)
    financial = models.BooleanField('Would like to be a financial partner', default=False)
    management = models.BooleanField('Would like to be a management partner', default=False)
    #partnership_type = models.CharField(max_length=255, choices=PARTNERSHIP_TYPE, default="", blank=True)
    active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('-created_on',)
        verbose_name = "Enterprise"
        verbose_name_plural = "Enterprises"
     
    @property
    def get_id(self):
        return self.id
    
    def get_absolute_url(self):
        return reverse("enterprises:enterprise-detail", kwargs={"slug": self.slug})
    
    def __str__(self):
        return self.user.email
    
def pre_save_enterprise(sender, instance, *args, **kwargs):
    if not instance.slug:
        #instance.slug = slugify(instance.user)
        instance.slug = slugify(f"{instance.company_name} {instance.id}")
           
def post_save_company(sender, instance, created, *args, **kwargs):
    if created:
        if instance.is_company:
            Enterprises.objects.create(
                user=instance, last_name=instance.last_name, first_name=instance.first_name,
            company_name=instance.company_name, email=instance.email, 
            is_company=instance.is_company, commercial=instance.commercial, technical=instance.technical, financial=instance.financial,
            management=instance.management
            )

class CompanyProfile(RandomIDModel):
    slug = models.SlugField(unique = True )
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, default="")
    last_name = models.CharField(max_length=100, default="")
    email = models.EmailField()
    company_name = models.CharField(max_length=50)
    company_type = models.CharField(max_length=50, choices=TYPE_COMPANIES, default = '')
    company_email = models.EmailField()
    company_address = models.CharField(max_length=255)
    company_city = models.CharField(max_length=100)
    company_country = models.CharField(max_length=255, choices=COUNTRIES)
    industry = models.ForeignKey(Industry, on_delete=models.SET_NULL, null=True)
    sector = models.ForeignKey(Sectors, on_delete=models.SET_NULL, null=True)
    company_web = models.CharField(max_length=255)
    phone_code = models.CharField(max_length=10, choices=PHONE_CODE)
    phone_number = models.CharField(max_length=10)
    number_employees = models.CharField(max_length=30, choices=EMP_NUMBER, default='')
    activity_description = models.TextField(max_length=500)
    annual_revenue = models.CharField(max_length = 50, choices=REVENUE, default='')
    is_company = models.BooleanField('Would like to register my company', default=False)
    commercial = models.BooleanField('Would like to be a commercial partner', default=False)
    technical = models.BooleanField('Would like to be a technical partner', default=False)
    financial = models.BooleanField('Would like to be a financial partner', default=False)
    management = models.BooleanField('Would like to be a management partner', default=False)
    active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('-created_on',)
        verbose_name = "Company Profile"
        verbose_name_plural = "Company Profiles"
    
    def __str__(self):
        return self.user.email
    
    @property
    def get_id(self):
        return self.id
    
    def get_absolute_url(self):
        return reverse("enterprises:enterprise-detail", kwargs={"slug": self.slug})
    
def pre_save_company(sender, instance, *args, **kwargs):
    if not instance.slug:
        #instance.slug = slugify(instance.user)
        #instance.slug = slugify(instance.company_name)
        instance.slug = slugify(f"{instance.company_name}-{instance.id}")
                 
def post_save_company_p(sender, instance, created, *args, **kwargs):
    if created:
        if instance.is_company:
            CompanyProfile.objects.create(user=instance, last_name=instance.last_name, first_name=instance.first_name,
            company_name=instance.company_name, email=instance.email, is_company=instance.is_company, 
        commercial=instance.commercial, technical=instance.technical, financial=instance.financial,
            management=instance.management)
        
#class FicheTechnic(RandomIDModel):
class FicheTechnic(models.Model):
    slug = models.SlugField(max_length = 20, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length = 768)
    category = models.CharField(max_length = 100, choices = FICHE_CAT)
    Expertise_level = models.CharField(max_length=100, choices=EXPERTISE_LEVEL)
    soil_climate = models.TextField(max_length=368, null=True)
    principal_risks = models.TextField(max_length=368, null=True, blank=True)
    season = models.CharField(max_length=100, null=True, blank=True)
    seeds = models.CharField(max_length = 50, null=True, blank=True)
    soil_preparation = models.TextField(max_length=368, null=True, blank=True)
    semis = models.TextField(max_length = 368, null=True, blank=True)
    care = models.TextField(max_length=368, null=True, blank=True)
    protection = models.TextField(max_length=368, null=True, blank=True)
    harvest = models.TextField(max_length=368, null=True, blank=True)
    post_harvest = models.TextField(max_length=368, null=True, blank=True)
    yield_harvest = models.TextField(max_length=160, null=True, blank=True)
    seed_supplier = models.TextField(max_length=200, null=True, blank=True)
    other_input = models.TextField(max_length=200, null=True, blank=True)
    equipment = models.TextField(max_length=200, null=True, blank=True)
    storage_requirements = models.TextField(max_length=200, null=True, blank=True)
    average_price = models.TextField(max_length=200, null=True, blank=True)
    marketing = models.TextField(max_length=200, null=True, blank=True)
    cost_acre = models.TextField(max_length=500, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "FicheTechnic"
        verbose_name_plural = "FicheTechnics"
        ordering = ('-created_on',)
    
          
    @property
    def get_id(self):
        return self.id
        
    def get_absolute_url(self):
        return reverse("fiches:fiche-detail", kwargs={'slug': self.slug})
          
    def __str__(self):
        return self.name
        
def pre_save_fiche(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(f"{instance.name} {instance.id}")
        
class Jobs(RandomIDModel):
#class Jobs(models.Model):
    slug = models.SlugField(unique=True)
    job_contact = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    email = models.EmailField(null=True, blank=True)
    company_name = models.CharField(max_length=50, blank=True, null=True)
    job_title = models.CharField(max_length=100)
    job_grade = models.CharField(choices=JOB_GRADES, max_length=2)
    Salary = models.FloatField()
    Department = models.CharField(choices=Departments, max_length=3)
    job_type = models.CharField(choices=JOB_TYPE, max_length=2)
    country = models.CharField(choices=COUNTRIES, max_length =2 )
    city = models.CharField(max_length = 50)
    summary = models.TextField(max_length=500)
    job_description = models.TextField(max_length=1000)
    job_qualifications = models.TextField(max_length=1000)
    travel_required = models.BooleanField(default=False)
    active = models.BooleanField(default = True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now = True)
    
    class Meta: 
        verbose_name = "Job"
        verbose_name_plural = "Jobs"
        ordering = ('-created_on',)
    
    def __str__(self):
        return f'{self.job_title}-{self.id}'
        
        
def pre_save_job(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(f"{instance.job_title} {instance.pk}")
        
class JobApplication(RandomIDModel):
#class JobApplication(models.Model):
    slug = models.SlugField(max_length=200, unique=True)
    user= models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE)
    email = models.EmailField(max_length=50)
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField()
    status = models.CharField(max_length=50, choices=APPLICATION_STATUS_CHOICES, default='Applied')
    created_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('-created_on',)
    
    def __str__(self):
        return f"{self.user.username} - {self.job.job_title}- {self.job.id}"
   
def pre_save_application(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(f"{instance.email} {instance.id}")

class Testimonies(RandomIDModel):
#class Testimonies(models.Model):
    slug = models.SlugField(max_length=200, unique=True)
    title = models.CharField(max_length=150)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    user_pic = models.ImageField(upload_to='document/', default='blog_pics/person_icon 1.png')
    #testimony = models.TextField()
    testimony = HTMLField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Testimony"
        verbose_name_plural = "Testimonies"
        ordering = ('-created_at',)

    def __str__(self):
        return f"{self.user}'s testimony"    

def pre_save_testimony(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(f"{instance.title} {instance.id}")
        
class Category(models.Model):
    name = models.CharField(max_length=50)
    
    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
        
    def __str__(self):
        return self.name
       
    
class Blog(RandomIDModel):
#class Blog(models.Model):
    slug = models.SlugField(max_length = 200, unique=True)
    title = models.CharField(max_length=200)
    categories = models.ManyToManyField(Category, related_name='blog')
    #content = RichTextField(blank=True, null=True )# to use rich text for blog post
    content = models.TextField(max_length = 5000)
    created_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    email = models.EmailField(null=True)
    blog_image = models.ImageField(upload_to='blog_pics', default='blog_pics/blogs.pnp')
    status = models.IntegerField(choices=BLOG_STATUS, default=0)
    
    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"
        ordering = ('-created_on',)
        
          
    @property
    def get_id(self):
        return self.id
     
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("blog-detail", kwargs={'slug': self.slug})

def pre_save_blog(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(f"{instance.title} {instance.id}")

class Review(RandomIDModel):
#class Review(models.Model):
    slug = models.SlugField(max_length = 200, unique=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='reviews', default="")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField(max_length = 768)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    created_on = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        ordering = ('-created_on',)
    '''
    @property
    def get_id(self):
        return self.id
    '''
    def __str__(self):
        return f"{self.user} - {self.blog.title}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.blog.average_rating = self.blog.reviews.aggregate(models.Avg('rating'))['rating__avg']
        self.blog.save()
    @property
    def get_id(self):
        return self.id
    
    def get_absolute_url(self):
        return reverse("review-detail", kwargs={'slug': self.slug})
    
def pre_save_review(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(f"{instance.blog} {instance.pk}")
    
class Deals(RandomIDModel):
    slug = models.SlugField(max_length = 200)
    dealer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="deals", null=True, blank=True)
    email = models.EmailField(null=True)
    company_name = models.CharField(max_length=50)
    category = models.CharField(max_length = 50, choices = OPP_CAT, default='')
    deal_title = models.CharField(max_length = 100)
    deal_type = models.CharField(max_length=50, choices = OPPORTUNITY_TYPES, default='')
    descriptions = models.TextField(max_length=750)
    deal_picture = models.FileField("Supporting Documents", upload_to='deals/', null=True, blank=True)
    active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now = True)

    class Meta:
        verbose_name = "Deal"
        verbose_name_plural = "Deals"
        ordering = ('-created_on',)
        
    @property
    def get_id(self):
        return self.id
        
    def __str__(self):
       return self.slug
   
    def get_absolute_url(self):
        return reverse("deals:deal-detail", kwargs={'slug': self.slug})

def pre_save_deal(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(f"{instance.deal_title} {instance.pk}")

class Rfi(RandomIDModel):
    slug = models.SlugField(max_length = 120, unique=True)
    deal = models.ForeignKey(Deals, on_delete=models.CASCADE)
    message = models.TextField()
    name = models.ForeignKey(CustomUser, on_delete = models.CASCADE, related_name='rfi')
    email = models.EmailField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now= True) 
    
    class Meta:
        verbose_name = "Rfi"
        verbose_name_plural = "Rfi"
        ordering = ('-created_on',)
    
    @property
    def get_id(self):
        return self.pk
          
    def __str__(self):
        return self.slug
     
def pre_save_rfi(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(f"{instance.deal} {instance.id}")

class Projects(RandomIDModel):
    slug = models.SlugField(max_length=200, null=False)
    project_name = models.CharField(max_length=100)
    company_name = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='projects')
    project_description = models.TextField()
    supporting_document = models.FileField(upload_to ='documents/', null=True,blank=True)
    reviewed = models.CharField(max_length = 10, choices = APPROVED, default='NO')
    reviewer_observations = models.TextField(default='', null=True, blank=True)
    #reviewed_by = models.CharField(max_length=50, null=True, blank=True)
    reviewed_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviewer', default='', null=True, blank=True)
    #reviewed_date = models.DateField(null=True, blank=True, auto_now=True)
    approved = models.CharField(max_length = 10, choices = APPROVED, default='NO')
    #approved_by = models.CharField(max_length=50, null=True, blank=True)
    approved_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='approver', default='', null=True, blank=True)
    approver_observations = models.TextField(default='', null=True, blank=True)
    #approved_date = models.DateField(null=True, blank=True, auto_now=True)
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('-created_on',)
        verbose_name = "Project"
        verbose_name_plural = "Projects"
    
    @property
    def get_id(self):
        return self.id
    
    def __str__(self):
        return self.project_name 
    

def pre_save_project(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(f"{instance.project_name} {instance.id}")
     

class Education(models.Model):
    slug = models.SlugField(max_length=200, null=False)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE )
    email = models.EmailField(null=True, blank=True)
    institution_name = models.CharField(pgettext_lazy("School Name", "school_name"),max_length=100)
    degree = models.CharField(choices=DEGREE_CHOICES, max_length=100, default="")
    specialization = models.CharField(max_length=255)
    minor = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField( blank=True, null=True)
    description = models.TextField(default='')
    graduated = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add = True)
    updated= models.DateTimeField( auto_now=True)
    class Meta: 
        verbose_name = "Education"
        verbose_name_plural = "Educations"
        ordering = ('-created_on',)
    
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    
    @property
    def get_id(self):
        return self.id
    
    @property
    def checkbox_character(self):
        return 'X' if self.graduated else ' '
    
    def __str__(self):
        return f"{self.degree} from {self.institution_name} ({self.start_date.year} - {self.end_date.year if self.end_date else 'Present'})"

def pre_save_education(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(f"{instance.institution_name} {instance.id}")

class Trainings(RandomIDModel):
    slug = models.SlugField(max_length=200, null=False)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE )
    teacher = models.CharField(max_length=50)
    email = models.EmailField()
    training_title = models.CharField(max_length=100, default='')
    training_type = models.CharField(max_length=100, choices=TRAININGS)
    domain = models.CharField(max_length=100, choices=TRAININGS_DOMAIN)
    duration = models.CharField(max_length=15,default='', choices=TRAININGS_DURATION)
    training_mode = models.CharField(max_length=20, choices=TRAININGS_MODE, default='')
    requirements = models.CharField(max_length=50, choices=REQUIREMENTS, default='')
    description = models.CharField(max_length=500)
    teacher_bio = models.CharField(max_length=500, default='')
    monday = models.BooleanField( default=False)
    tuesday = models.BooleanField( default=False)
    wednesday = models.BooleanField(default=False)
    thursday = models.BooleanField(default=False)
    friday = models.BooleanField(default=False)
    saturday = models.BooleanField(default=False)
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    cost = models.FloatField()
    certification = models.BooleanField("Will this course deliver a certificate?", default=False)
    active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now = True)
    
    class Meta: 
        verbose_name = "Training"
        verbose_name_plural = "Trainings"
        ordering = ('-created_on',)
        
    @property
    def get_id(self):
        return self.id
    
    def __str__(self):
        return self.training_title
    
def pre_save_training(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(f"{instance.training_title} {instance.id}")    

class TrainingApplication(RandomIDModel): 
    slug = models.SlugField(max_length=200, unique=True)
    name= models.CharField(max_length=255)
    training = models.ForeignKey(Trainings, on_delete=models.CASCADE)
    email = models.EmailField(max_length=50)
    phone_code = models.CharField(max_length=10, choices=PHONE_CODE)
    phone_number = models.CharField(max_length=10)
    company_name = models.CharField(max_length=100, default='')
    position = models.CharField(max_length= 30, choices=POSITIONS)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    #letter = models.TextField()
    member = models.BooleanField(default=False)
    status = models.CharField(max_length=50, choices=APPLICATION_STATUS_CHOICES, default='Applied')
    created_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('-created_on',)
    
    @property
    def get_id(self):
        return self.id
     
    def __str__(self):
        return f"{self.email}- {self.id}"
   
def pre_save_training_application(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(f"{instance.name} {instance.id}")


#post_save.connect(post_save_user, sender=Subscription )
pre_save.connect(pre_save_employee, sender=Employee)
pre_save.connect(pre_save_job, sender=Jobs)
pre_save.connect(pre_save_application, sender=JobApplication)
pre_save.connect(pre_save_expert, sender=Experts)
pre_save.connect(pre_save_expert_p, sender=ExpertProfile)
pre_save.connect(pre_save_product, sender=Product)
post_save.connect(post_save_expert, sender=CustomUser )
#post_save.connect(post_save_employee, sender=CustomUser )
post_save.connect(post_save_expert_p, sender=CustomUser )
#post_save.connect(post_save_employee_p, sender=CustomUser )
pre_save.connect(pre_save_testimony, sender=Testimonies)
post_save.connect(post_save_company_p, sender=CustomUser)
post_save.connect(post_save_company, sender=CustomUser)
pre_save.connect(pre_save_deal, sender=Deals)
pre_save.connect(pre_save_project, sender=Projects)
pre_save.connect(pre_save_company, sender=CompanyProfile)
pre_save.connect(pre_save_fiche, sender=FicheTechnic)
pre_save.connect(pre_save_blog, sender=Blog)
pre_save.connect(pre_save_rfi, sender=Rfi)
pre_save.connect(pre_save_enterprise, sender=Enterprises)
pre_save.connect(pre_save_review, sender=Review)
pre_save.connect(pre_save_education, sender=Education)
pre_save.connect(pre_save_employee_p, sender=EmployeeProfile)
pre_save.connect(pre_save_training, sender=Trainings)
pre_save.connect(pre_save_training_application, sender=TrainingApplication)
