from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
#from common.utils import *
from django.dispatch import receiver
from django.db.models.signals import post_save

PARTNERSHIP_TYPE = (('COMMERCIAL', 'COMMERCIAL'),
                     ('TECHNIQUE', 'TECHNIQUE'),
                     ('FINANCIER', 'FINANCIER'),
                     ('MANAGEMENT', 'MANAGEMENT'))

class CustomUser(AbstractUser):
    company_name = models.CharField(max_length=100, default="")
    COMPANY = 'COMPANY'
    EXPERT = 'EXPERT'
    #EMPLOYEE = 'EMPLOYEE'
    #ADMIN = 'ADMIN'
    USER_CHOICES = ( (COMPANY, 'COMPANY'), (EXPERT, 'EXPERT'), )
    #user_type = models.CharField(choices=USER_CHOICES, max_length=12, default="")
    is_admin = models.BooleanField('Is Admin', default=False)
    is_expert = models.BooleanField('Would like to share my expertise', default=False)
    is_company = models.BooleanField('Would like to register my company', default=False)
    is_employee = models.BooleanField('Is Employee', default=False)
    commercial = models.BooleanField('Would like to be a commercial partner', default=False)
    technical = models.BooleanField('Would like to be a technical partner', default=False)
    financial = models.BooleanField('Would like to be a financial partner', default=False)
    management = models.BooleanField('Would like to be a management partner', default=False)
    is_reviewer = models.BooleanField('Is reviewer', default=False)
    is_approver = models.BooleanField('Is approver', default=False)
    #partnership_type = models.CharField('What type of partnership do you want to establish? ',choices=PARTNERSHIP_TYPE, max_length=50, default='')
        
    class Meta:
        ordering = ('id',)   
        
        '''
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
     
class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        ('C', 'Company'),
        ('E', 'Expert'),
        ('P', 'Employee'),
        ('A', 'Admin'),
    )
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=1, choices=USER_TYPE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_type']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        '''
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