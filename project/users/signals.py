from django.db import models
from django.dispatch import receiver

from users.models import User, Profile


@receiver(models.signals.post_save, sender=User)
def post_save_user_signal_handler(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)