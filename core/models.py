from django.db import models
from django.shortcuts import reverse
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from common.utils import *
import re
from django.utils.text import slugify
#from accounts.models import CustomUser
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
#from common.utils import *

from django.db.models.signals import post_save
from django.utils.translation import pgettext_lazy, gettext_lazy as _
from datetime import datetime
from django.conf import settings
from django.utils import timezone
from django_random_id_model import RandomIDModel
from django.dispatch import receiver
import stripe
from PIL import Image
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

PARTNERSHIP_TYPE = (('COMMERCIAL', 'COMMERCIAL'),
                     ('TECHNIQUE', 'TECHNIQUE'),
                     ('FINANCIER', 'FINANCIER'),
                     ('MANAGEMENT', 'MANAGEMENT'))
SALUTATIONS = (("MISS","MISS"), ("Mrs","Mrs"), ("Ms", "Ms"), ("Mr", "Mr"))
class CustomUser(AbstractUser):
    company_name = models.CharField(max_length=100, default="")
    COMPANY = 'COMPANY'
    EXPERT = 'EXPERT'
    #EMPLOYEE = 'EMPLOYEE'
    #ADMIN = 'ADMIN'
    USER_CHOICES = ( (COMPANY, 'COMPANY'), (EXPERT, 'EXPERT'), )
    salutations = models.CharField(max_length=10, choices=SALUTATIONS, default="")
    #user_type = models.CharField(choices=USER_CHOICES, max_length=12, default="")
    is_admin = models.BooleanField('Is Admin', default=False)
    is_expert = models.BooleanField('Would like to register as an expertise', default=False)
    #is_company = models.BooleanField('Would like to register my company', default=False)
    is_employee = models.BooleanField('Is Employee', default=False)
    commercial = models.BooleanField('Would like to be a commercial partner', default=False)
    technical = models.BooleanField('Would like to be a technical partner', default=False)
    financial = models.BooleanField('Would like to be a financial partner', default=False)
    management = models.BooleanField('Would like to be a management partner', default=False)
    is_reviewer = models.BooleanField('Is reviewer', default=False)
    is_approver = models.BooleanField('Is approver', default=False)
    agreement = models.BooleanField('By clicking I accept to become member and share my information with your organization', default=False)
    #partnership_type = models.CharField('What type of partnership do you want to establish? ',choices=PARTNERSHIP_TYPE, max_length=50, default='')
        
    class Meta:
        ordering = ('id',)   
        

class ContactUs(models.Model):

    name = models.CharField(max_length=50)
    email = models.CharField(max_length = 50)
    phone_ind= models.CharField(max_length=3)
    phone_number = models.CharField(max_length=10)
    message = models.CharField(max_length = 500)
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField( auto_now=True)
   
    class Meta: 
        verbose_name = "Contacts"
        verbose_name_plural = "Contacts"
        ordering = ('-created_on',)
    
    def __str__(self):
        return self.name
    
    
class Pricing(models.Model):
    name = models.CharField(_('pricing tier'), max_length=100) # free / basic / pro
    
    def __str__(self):
        return self.name
    

class Subscription(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=5)
    #pricing = models.ForeignKey(Pricing, on_delete=models.CASCADE, related_name='subscriptions', null=True, blank=True)# query = P
    stripe_product_id = models.CharField(max_length=50, default="")
    status = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    
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
    slug = models.SlugField(unique=True, null=True)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, default="")
    description = models.CharField(max_length=255, default="")
    product_features = models.CharField(max_length=255, default="")
    monthly_price = models.PositiveIntegerField(default=0) # cents 1000 = $10.00 while in stripe
    yearly_price = models.PositiveIntegerField(default=0) # cents 1000 = $10.00 while in stripe 
    monthly_link = models.URLField(default='')
    yearly_link = models.URLField(default='')
    created_on = models.DateTimeField(auto_now_add=True)
    
    class Meta: 
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ('monthly_price',)
    
    def __str__(self):
        return self.name
    
    
    def get_display_price(self):
        return "{0:.2f}".format(self.price / 100)# get dollars and round to 2 decimals
    
    
def pre_save_product(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)        
    


class AdminProfile(RandomIDModel):
    slug = models.SlugField(unique=True)
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, default="")
    last_name = models.CharField(max_length=100, default="")
    DOB = models.DateField(null=True, blank=True)
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
    first_name = models.CharField(max_length=100, default="")
    last_name = models.CharField(max_length=100, default="")
    DOB = models.DateField(null=True, blank=True)
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
    hired_date = models.DateField(null=True, blank=True)
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
     
def post_save_employee_p(sender, instance, created, *args, **kwargs):
    if created:
        if instance.is_employee:
            EmployeeProfile.objects.create(user=instance, last_name = instance.last_name, first_name = instance.first_name, 
                                     email = instance.email
            )

#class ExpertProfile(RandomIDModel):
class ExpertProfile(models.Model):
    slug = models.SlugField(unique=True)
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, default="")
    last_name = models.CharField(max_length=100, default="")
    DOB = models.DateField("Enter Your Date of Birth", null=True, blank=True)
    company_name = models.CharField(max_length=50, null=True, blank=True)
    avatar = models.ImageField(upload_to='document/', default='document/person_icon_1.png')
    #avatar = models.ImageField(
        #default='document/person_icon 1.png', # default avatar
        #upload_to='profile_avatars/' # dir to store the image
   # )
    street_address = models.CharField(max_length=50, default="", null=True, blank=True)
    city = models.CharField(max_length = 66, default="")
    state = models.CharField( max_length = 2, default="", null=True, blank=True)
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
    
    def get_absolute_url(self):
        return reverse("profiles:expert-detail", kwargs={"slug": self.slug})
    
    @property
    def get_id(self):
        return self.id
    
    def __str__(self):
        return self.email
    
    '''
    def save(self, *args, **kwargs):
        # save the profile first
        super().save(*args, **kwargs)

        # resize the image
        img = Image.open(self.avatar.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            # create a thumbnail
            img.thumbnail(output_size)
            # overwrite the larger image
            img.save(self.avatar.path)
'''
def pre_save_expert_p(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(f"{instance.user}-{instance.id}")
        
def post_save_expert_p(sender, instance, created, *args, **kwargs):
    if created:
        if instance.is_expert:
            ExpertProfile.objects.create(user=instance, last_name = instance.last_name, first_name = instance.first_name, company_name = instance.company_name, email = instance.email, commercial=instance.commercial, technical=instance.technical, financial=instance.financial, management=instance.management
                                     )

class Industry(models.Model):
    name = models.CharField( max_length=200, )
    description = models.TextField(max_length=255)
    #created_on = models.DateTimeField(auto_now_add = True)
    #updated_on = models.DateTimeField(auto_now = True)
    
    class Meta:
        #ordering = ('-created_on',)
        verbose_name = "Industry"
        verbose_name_plural = "Industries"
    
    def __str__(self):
        return self.name

class Sectors(models.Model):
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE, related_name='sectors')
    name = models.CharField(max_length=100, default="", null=True)
    description = models.TextField(max_length=500)
    #created_on = models.DateTimeField(auto_now_add=True)
    #updated_on = models.DateTimeField(auto_now=True)
    
    class Meta:
        
        #ordering = ('-created_on',)
        verbose_name = "Sector"
        verbose_name_plural = "Sectors"
    
    def __str__(self):
        return self.name
    
class Enterprises(RandomIDModel):
#class Enterprises(models.Model):
    slug = models.SlugField(unique = True )
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE, default='')
    company_logo = models.ImageField(upload_to='document/', default='document/maze_field.jpeg')
    company_email = models.EmailField()
    registration_id = models.CharField(max_length=50, default="", null=True)
    registration_date = models.DateField(null=True)
    company_name = models.CharField(max_length=50)
    company_type = models.CharField(max_length=50, choices=TYPE_COMPANIES, default = '')
    company_address = models.CharField(max_length=255)
    company_city = models.CharField(max_length=100)
    company_country = models.CharField(max_length=255, choices=COUNTRIES)
    industry = models.ForeignKey(Industry, on_delete=models.SET_NULL, null=True)
    sector = models.ForeignKey(Sectors, on_delete=models.SET_NULL, null=True)
    company_web = models.CharField(max_length=255)
    commercial = models.BooleanField('Would like to be a commercial partner', default=False)
    technical = models.BooleanField('Would like to be a technical partner', default=False)
    financial = models.BooleanField('Would like to be a financial partner', default=False)
    management = models.BooleanField('Would like to be a management partner', default=False)
    phone_code = models.CharField(max_length=10, choices=PHONE_CODE)
    phone_number = models.CharField(max_length=10)
    number_employees = models.CharField(max_length=15, choices=EMP_NUMBER, default='0_10')
    annual_revenue = models.CharField(max_length = 50, choices=REVENUE, default='0_150 000 000')
    currency= models.CharField(max_length=50, choices=CURRENCIES_SYMBOLS, default='')
    activity_description = models.TextField("Tell us more about your company's activities ", max_length=3500)
   
    #is_company = models.BooleanField('Would like to register my company', default=False)
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
        return self.company_name
    
def pre_save_enterprise(sender, instance, *args, **kwargs):
    if not instance.slug:
        #instance.slug = slugify(instance.user)
        instance.slug = slugify(f"{instance.company_name} {instance.id}")
           
def post_save_company(sender, instance, created, *args, **kwargs):
    if created:
        if instance.is_expert:
            Enterprises.objects.create(
                user=instance, company_name=instance.company_name, commercial=instance.commercial, technical=instance.technical, financial=instance.financial, management=instance.management
            )
  
class FicheTechnic(RandomIDModel):
#class FicheTechnic(models.Model):
    slug = models.SlugField(max_length = 20, unique=True)
    name = models.CharField(max_length=100)
    fiche_avatar = models.ImageField(upload_to='document/', default='document/maze_field.jpeg')
    description = models.TextField(max_length = 4500)
    category = models.CharField(max_length = 100, choices = FICHE_CAT)
    Expertise_level = models.CharField(max_length=100, choices=EXPERTISE_LEVEL)
    Technical_factors = models.TextField("This include climate,season, soil preparation,seeds, semis, care, conditions, and protection",max_length=4500, null=True, blank=True)
    principal_risks = models.TextField(max_length=3368, null=True, blank=True)
    harvest_factors = models.TextField("Include how to harvest, post harvest conditioning, yield", max_length=4500, null=True, blank=True)
    marketing_factor = models.TextField("include seed supplier, equipment cost, storage requirements, average price per unit (acre, kilo, tone...), average cost ", max_length=4500, null=True, blank=True)
    industrialization_factors = models.TextField("what to consider if industrializing", max_length=4500, null=True, blank=True) 
    other_factors = models.TextField("Import Export opportunities, main producers, main consumers...", max_length=5100, null=True, blank=True)
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
        
class FicheRead(models.Model):
    reader = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    fiche_read = models.ForeignKey(FicheTechnic, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('reader', 'fiche_read')
        
    def __str__(self):
       return f"{self.reader} - {self.fiche_read}" 
class Jobs(RandomIDModel):
#class Jobs(models.Model):
    slug = models.SlugField(unique=True)
    job_contact = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    email = models.EmailField(null=True, blank=True)
    company_name = models.CharField(max_length=50, blank=True, null=True)
    job_title = models.CharField(max_length=100)
    job_grade = models.CharField(choices=JOB_GRADES, max_length=2)
    Salary = models.FloatField()
    currency= models.CharField(max_length=50, choices=CURRENCIES_SYMBOLS, default='') 
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
        
class JobRead(models.Model):
    reader = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    job_read = models.ForeignKey(Jobs, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('reader', 'job_read')
        ordering = ('-timestamp',) 
    def __str__(self):
       return f"{self.reader} - {self.job_read}" 
     
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
    description = models.CharField(max_length=250, blank=True, null=True)
    
    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
        
    def __str__(self):
        return self.name
       
    
class Blog(RandomIDModel):
#class Blog(models.Model):
    slug = models.SlugField(max_length = 200, unique=True)
    title = models.CharField(max_length=200)
    #categories = models.CharField(choices=BLOG_CATEGORIES, max_length=50, default='')
    categories = models.ForeignKey(Category, on_delete=models.CASCADE, related_name = 'blog', default='')
    content = RichTextField()# to use rich text for blog post
    #content = models.TextField(max_length = 5000)
    created_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    email = models.EmailField(null=True)
    blog_image = models.ImageField(upload_to='blog_pics/', default='blog_pics/blog 1.pnp')
    status = models.CharField(max_length=15, choices=BLOG_STATUS, default="DRAFT")
    
    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"
        ordering = ('-created_on',)
        
    @staticmethod
    def count_blogs_by_status():
        return {
            'Draft': Blog.objects.filter(status="DRAFT").count(),
            'Published': Blog.objects.filter(status="PUBLISHED").count(),
            'Archived': Blog.objects.filter(status="ARCHIVED").count(),
        }

    def __str__(self):
        return self.title
      
    @property
    def get_id(self):
        return self.id
    
    @property 
    def blog_length(self):
        blog_length = len(self.content)
        blog_length = len(re.findall(r'\w+', self.content))
        return blog_length
        
    @property 
    def blog_time(self):
        blog_time = round((len(re.findall(r'\w+', self.content))/200),2)
        return blog_time
     
    def get_average_rating(self):
        reviews = self.review_set.all()
        if reviews:
            return sum([review.rating for review in reviews]) / reviews.count()
        return 0
    
    def get_absolute_url(self):
        return reverse("blog-detail", kwargs={'slug': self.slug})

def pre_save_blog(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(f"{instance.title} {instance.id}")


class BlogRead(models.Model):
    reader = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    blog_post = models.ForeignKey(Blog, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('reader', 'blog_post')
        ordering = ('-timestamp',)
        
    def __str__(self):
       return f"{self.reader} - {self.blog_post}"
        
class Review(RandomIDModel):
#class Review(models.Model):
    slug = models.SlugField(max_length = 200, unique=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='reviews', default="")
    reviewer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.TextField(max_length = 768)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    created_on = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        ordering = ('-created_on',)
    
    @property 
    def review_metrics(self):
        average_review = sum(self.rating)/self.slug.count()
        number_review = self.slug.count()
        
       
        return average_review, number_review
    @property
    def get_id(self):
        return self.id
    
    def __str__(self):
        return f"{self.reviewer.username}'s review of {self.blog.title}"
    '''
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.blog.average_rating = self.blog.reviews.aggregate(models.Avg('rating'))['rating__avg']
        self.blog.number_of_reviews = self.blog.reviews.aggregate(models.count('rating')['rating_count'])
        self.blog.save()
        '''
    @property
    def get_id(self):
        return self.id
    
    def get_absolute_url(self):
        return reverse("review-detail", kwargs={'slug': self.slug})
    
def pre_save_review(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(f"{instance.blog} {instance.pk}")

#class ReplyToComment(models.Model):
class ReplyToReview(RandomIDModel):
    slug = models.SlugField(max_length = 200, unique=True, null=True, blank=True)
    review = models.ForeignKey(Review, related_name='replies', on_delete=models.CASCADE)
    replier = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "ReplyToReview"
        verbose_name_plural = "ReplyToReviews"
        ordering = ('-created_on',)

    def __str__(self):
        return f'Reply by {self.replier} on {self.review}'
    
    @property
    def get_id(self):
        return self.id
    def get_absolute_url(self):
        return reverse("blogs:review-detail", kwargs={'slug': self.slug})

def pre_save_reply_to_review(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(f"{instance.review_id} {instance.pk}")
        
             
class Deals(RandomIDModel):
    slug = models.SlugField(max_length = 200)
    dealer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="deals", null=True, blank=True)
    service_category= models.CharField(max_length=100, choices=SERVICES_CATEGORIES, default='')
    deal_type = models.CharField(max_length=50, choices = OPPORTUNITY_TYPES, default='')
    email = models.EmailField(null=True)
    company_name = models.CharField(max_length=50)
    #deal_category = models.CharField(max_length = 50, choices = SERVICES_CATEGORIES, default='')
    deal_title = models.CharField(max_length = 100)
    deal_country = models.CharField(choices=COUNTRIES, max_length =2, default='')
    deal_city = models.CharField(max_length=100, default='')
    descriptions = models.TextField(max_length=750) 
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

class DealImages(models.Model):
    deal = models.ForeignKey(Deals, on_delete=models.CASCADE)
    image = models.FileField("Supporting Documents", upload_to='deals/', default='deals/deals.jpeg')
    
class DealRead(models.Model):
    reader = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    deal_read = models.ForeignKey(Deals, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('reader', 'deal_read')
        ordering = ('-timestamp',)
        
    def __str__(self):
       return f"{self.reader} - {self.deal_read}"
    
class Rfi(RandomIDModel):
    slug = models.SlugField(max_length = 120, unique=True)
    deal = models.ForeignKey(Deals, on_delete=models.CASCADE)
    message = models.TextField(max_length=5000)
    client_name = models.ForeignKey(CustomUser, on_delete = models.CASCADE, related_name='rfi')
    client_email = models.EmailField()
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
    project_initiator = models.ForeignKey(CustomUser, related_name="owner", on_delete=models.CASCADE, null=True, blank=True)
    project_name = models.CharField(max_length=100)
    project_category = models.CharField(max_length=50, choices=PROJECT_CATEGORY, default='')
    company_name = models.ForeignKey(Enterprises, on_delete=models.CASCADE, related_name='projects')
    project_description = models.TextField()
    estimated_cost = models.PositiveIntegerField('Estimated Cost in US $',)
    estimated_Annual_revenue = models.PositiveIntegerField('Estimated Annul Revenue in US $')
    supporting_document = models.FileField(upload_to ='documents/', null=True,blank=True)
    reviewed = models.BooleanField(default=False)
    reviewer_observations = models.TextField(default='', null=True, blank=True)
    reviewed_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name='reviewer', default='', null=True, blank=True)
    approved = models.BooleanField( default=False)
    approved_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name='approver', default='', null=True, blank=True)
    approver_observations = models.TextField(default='', null=True, blank=True)
    final_decision = models.CharField(max_length=15, choices=PROJECT_DECISION, default='')
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
     

#class Education(models.Model):

class Trainings(RandomIDModel):
    slug = models.SlugField(max_length=200, null=False)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE )
    teacher = models.CharField(max_length=50)
    email = models.EmailField()
    training_title = models.CharField(max_length=100, default='')
    training_type = models.CharField(max_length=100, choices=TRAININGS)
    domain = models.CharField(max_length=100, choices=TRAININGS_DOMAIN)
    venue_address = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100, default='')
    country = models.CharField(max_length=100, choices=COUNTRIES, default='')
    duration = models.CharField(max_length=15,default='', choices=TRAININGS_DURATION)
    training_mode = models.CharField(max_length=20, choices=TRAININGS_MODE, default='')
    requirements = models.CharField(max_length=50, choices=REQUIREMENTS, default='')
    description = models.TextField(max_length=500)
    teacher_bio = models.TextField(max_length=500, default='')
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
    currency= models.CharField(max_length=50, choices=CURRENCIES_SYMBOLS, default='')
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
    updated_on = models.DateTimeField(auto_now=True)
    
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

### ANNOUNCEMENTS Services and products
#class ProductDeals(models.Model):
class ProductDeals(RandomIDModel):
    slug = models.SlugField(max_length = 120, unique=True)
    email = models.EmailField(null=True)
    dealer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="product_deals", null=True, blank=True)
    product_deal_title = models.CharField(max_length = 100)
    opportunity_type = models.CharField(max_length=50, choices=PRODUCTS_OPPORTUNITIES)
    company_name = models.CharField(max_length=50, default='')
    product_name = models.CharField(max_length=255)
    product_category= models.CharField('Enter Your Product Category',max_length=100, choices=PRODUCTS_CATEGORIES, )
    product_description = models.TextField()
    #product_image = models.ImageField(upload_to='products/images/', default='deals/deals.jpeg')
    city = models.CharField(max_length=100, default='')
    country = models.CharField(max_length=100, choices=COUNTRIES)
    availability_date = models.DateField() 
    stock_quantity = models.PositiveIntegerField(null=True, blank=True)
    quantity_unit = models.CharField(max_length=100, choices=MEASUREMENT_UNIT, default='')
    is_available = models.BooleanField(default=True)
    announcement_date = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField('Price Per Unit',max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=100, choices=CURRENCIES_SYMBOLS, null=True, blank=True)
    discount = models.CharField(max_length=5, choices=DISCOUNTS, null=True, blank=True)
    #tags = models.ManyToManyField('Tag', blank=True)
    notes = models.TextField(blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    class Meta: 
        verbose_name = "Product Deal"
        verbose_name_plural = "Product Deals"
        ordering = ('-announcement_date',)
        
    def __str__(self):
        return self.product_deal_title

def pre_save_product_deals(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(f"{instance.product_name} {instance.id}")

class ProductDealImages(models.Model):
    deal = models.ForeignKey(ProductDeals, on_delete=models.CASCADE)
    image = models.FileField("Supporting Documents", upload_to='deals/', default='deals/deals.jpeg')


class ProductDealRead(models.Model):
    reader = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product_deal_read = models.ForeignKey(ProductDeals, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('reader', 'product_deal_read')
        ordering = ('-timestamp',)
        
    def __str__(self):
       return f"{self.reader} - {self.product_deal_read}" 
class ProductRFI (RandomIDModel):
    slug = models.SlugField(max_length = 120, unique=True)
    product_deal = models.ForeignKey(ProductDeals, on_delete=models.CASCADE)
    message = models.TextField(max_length=5000)
    client_name = models.ForeignKey(CustomUser, on_delete = models.CASCADE, related_name='product_rfi')
    client_email = models.EmailField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now= True) 
    class Meta: 
        verbose_name = "Product rfi"
        verbose_name_plural = "Product rfi"
        ordering = ('-created_on',)
        
    def __str__(self):
        return self.slug

def pre_save_product_rfi(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(f"{instance.product_deal} {instance.id}")
    

#class WorkExperience(models.Model):
class WorkExperience(RandomIDModel):
    # A foreign key to associate experience with a specific employee
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    work_location_address = models.CharField(max_length=100)
    work_city = models.CharField("Enter the City where the work is located", max_length=100)
    work_country = models.CharField(max_length=50, choices=COUNTRIES)
    job_title = models.CharField("Enter Your Job Title",max_length=100, default="")
    position = models.CharField("Enter Your Position" ,max_length=100)
    start_date = models.DateField("Enter the starting date of this position")
    end_date = models.DateField("Enter the end date of this position. If still in the position leave it blank",null=True, blank=True)  # Allow null for current job
    description = models.TextField(blank=True)
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)
    
    class Meta: 
        verbose_name = "Work history"
        verbose_name_plural = "Work history"
        ordering = ('-start_date',)

    def __str__(self):
        return f"{self.position} at {self.company_name}"
'''
def pre_save_work_experience(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(f"{instance.position} {instance.company_name}")    
'''

class ExpertPortfolio(models.Model):
    # A foreign key to associate a project with a specific consultant
    consultant = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='projects')
    #consultant_email = models.EmailField(null=True, blank=True)
    # Project Details
    project_title = models.CharField(max_length=200)
    project_type = models.CharField(max_length=200, default="")
    project_city = models.CharField(max_length=100, default='')
    project_country = models.CharField(max_length=50, choices=COUNTRIES, default='')
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)  # Allow null for ongoing projects
    client_name = models.CharField(max_length=200)
    reference_email= models.EmailField()
    technologies_used = models.CharField(max_length=300)  # Can be replaced with a many-to-many relationship if needed
    created_on = models.DateTimeField(auto_now_add = True)
    
    class Meta: 
        verbose_name = "Expert portfolio"
        verbose_name_plural = "Expert portfolios"
        ordering = ('-start_date',)
     
    def __str__(self):
        return self.project_title
  
  
class Education(RandomIDModel):
    slug = models.SlugField(max_length=200, null=False)
    student=models.ForeignKey(CustomUser,on_delete=models.CASCADE )
    #student_email = models.EmailField(null=True, blank=True)
    institution_name = models.CharField(pgettext_lazy("School Name", "school_name"),max_length=100)
    degree = models.CharField(choices=DEGREE_CHOICES, max_length=100, default="")
    specialization = models.CharField(max_length=255)
    minor = models.CharField(max_length=255)
    start_date = models.DateField("Enter Your Degree Starting Date")
    end_date = models.DateField("Enter Your Degree Ending Date", blank=True, null=True)
    gpa = models.FloatField("Enter Your Grade Point Average")
    graduated = models.BooleanField(default=False)
    description = models.TextField(default='')
    created_on = models.DateTimeField(auto_now_add = True)
    updated= models.DateTimeField( auto_now=True)
    class Meta: 
        verbose_name = "Education"
        verbose_name_plural = "Educations"
        ordering = ('-start_date',)
    
    @property
    def get_name(self):
        return self.user
    
    @property
    def get_id(self):
        return self.id
    
    @property
    def checkbox_character(self):
        return 'X' if self.graduated else ' '
    
    def __str__(self):
        return f"{self.degree} from {self.institution_name} ({self.start_date.year} - {self.end_date.year if self.end_date else 'Present'})"

class ExpertMessaging(RandomIDModel):
    expert = models.ForeignKey(ExpertProfile, on_delete=models.CASCADE, related_name="message_receiver")
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='message_sender')
    sender_email = models.EmailField()
    subject = models.CharField(max_length=250)
    content = models.TextField()
    attached_file = models.FileField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    class Meta: 
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ('-created_on',)
    
    @property
    def get_id(self):
        return self.id
     
    def __str__(self):
        return self.subject

#parent model
#class forum(models.Model):
class Forum(RandomIDModel):
    slug = models.SlugField(max_length=200, null=False)
    forum_creator=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    creator_email = models.EmailField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    topic= models.CharField(max_length=300)
    description = models.TextField(max_length=1000,blank=True)
    link = models.CharField(max_length=100 ,null =True)
    active = models.BooleanField(default=False)
    created_on=models.DateTimeField(auto_now_add=True,null=True)
    
    class Meta: 
        verbose_name = "forum"
        verbose_name_plural = "forums"
        ordering = ('-created_on',)
    
    @property
    def get_id(self):
        return self.id
    
    def __str__(self):
        return str(self.topic)
     
def pre_save_forum(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(f"{instance.topic} {instance.id}")
 
#child model
class Discussion(models.Model):
    slug = models.SlugField(max_length=200, null=False)
    discussion_creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    discussion_email = models.EmailField(null=True, blank=True)
    forum = models.ForeignKey(Forum,on_delete=models.CASCADE)
    discuss = models.TextField()
    created_on=models.DateTimeField(auto_now_add=True,null=True)

    class Meta: 
            verbose_name = "Discussion"
            verbose_name_plural = "Discussions"
            ordering = ('-created_on',)
    
    @property
    def get_id(self):
        return self.id
    
    def __str__(self):
        return str(self.discussion_creator)
    
    
def pre_save_discussion(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(f"{instance.discussion_creator} {instance.id}")

pre_save.connect(pre_save_forum, sender=Forum)
pre_save.connect(pre_save_discussion, sender=Discussion)  
#post_save.connect(post_save_user, sender=Subscription )
#pre_save.connect(pre_save_employee, sender=Employee)
pre_save.connect(pre_save_product_deals, sender=ProductDeals)
pre_save.connect(pre_save_product_rfi, sender=ProductRFI)
pre_save.connect(pre_save_job, sender=Jobs)
pre_save.connect(pre_save_application, sender=JobApplication)
pre_save.connect(pre_save_expert_p, sender=ExpertProfile)
pre_save.connect(pre_save_product, sender=Product)
post_save.connect(post_save_admin_p, sender=CustomUser )
pre_save.connect(pre_save_admin_p, sender=AdminProfile)
#post_save.connect(post_save_employee, sender=CustomUser )
post_save.connect(post_save_expert_p, sender=CustomUser )
post_save.connect(post_save_employee_p, sender=CustomUser )
pre_save.connect(pre_save_testimony, sender=Testimonies)
post_save.connect(post_save_company, sender=CustomUser)
pre_save.connect(pre_save_deal, sender=Deals)
pre_save.connect(pre_save_project, sender=Projects)
pre_save.connect(pre_save_fiche, sender=FicheTechnic)
pre_save.connect(pre_save_blog, sender=Blog)
pre_save.connect(pre_save_rfi, sender=Rfi)
pre_save.connect(pre_save_enterprise, sender=Enterprises)
pre_save.connect(pre_save_review, sender=Review)
pre_save.connect(pre_save_reply_to_review, sender=ReplyToReview)
#pre_save.connect(pre_save_education, sender=Education)
pre_save.connect(pre_save_employee_p, sender=EmployeeProfile)
pre_save.connect(pre_save_training, sender=Trainings)
pre_save.connect(pre_save_training_application, sender=TrainingApplication)
