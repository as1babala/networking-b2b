from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import *

@receiver(post_save, sender=CustomUser)
def create_expert(sender, instance, created, **kwargs):
    if created and instance.user_type == 'EXPERT':
        Experts.objects.create(user=instance)
