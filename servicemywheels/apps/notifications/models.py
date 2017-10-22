from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


class Notifications(models.Model):
    title = models.CharField(max_length=256)
    message = models.TextField()
    viewed = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)


@receiver(post_save, sender=User)
def create_welcome_message(sender, **kwargs):
    if kwargs.get('created', False):
        Notifications.objects.create(user=kwargs.get('instance'),
                                    title="Welcome to ServiceMyWheels",
                                    message="Thanks for signup!!")