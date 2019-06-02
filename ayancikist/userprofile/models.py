from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils.text import slugify


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user')
    # add PhotoField later
    website = models.URLField(default='', blank=True)
    bio = models.TextField(default='', blank=True)
    phone = models.CharField(max_length=14, blank=True, default='')
    # maybe add a dropdown list for city choice later?
    city = models.CharField(max_length=100, blank=True, default='')

    def __str__(self):
        return self.user
