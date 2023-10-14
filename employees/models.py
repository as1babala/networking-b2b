from django.db import models
from django.shortcuts import reverse
from django.db.models.signals import pre_save, post_save
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
#from django_extensions.db.fields import RandomPrimaryKey
import shortuuid
from django.core.exceptions import ValidationError
#from phonenumber_field.modelfields import PhoneNumberField
import stripe
#stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your models here.
