from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils.text import slugify

# Import the model from 'accounts.forms' to include this
# model on a new form that is for user registration.
class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    # add PhotoField later
    website = models.URLField(default='', blank=True)
    bio = models.TextField(default='', blank=True)
    phone = models.CharField(max_length=14, blank=True, default='')
    # maybe add a dropdown list for city choice later?
    city = models.CharField(max_length=100, blank=True, default='')
    # dropdown?
    country = models.CharField(max_length=100, default='', blank=True)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return "{}'s profile page".format(self.user)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
