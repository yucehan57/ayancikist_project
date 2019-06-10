from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Import the model from 'accounts.forms' to include this
# model on a new form that is for user registration.
class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='userprofiles',
                                on_delete=models.CASCADE)
    # add PhotoField later
    website = models.URLField(default='', blank=True)
    bio = models.TextField(default='', blank=True)
    phone = models.CharField(max_length=14, blank=True, default='')
    # maybe add a dropdown list for city choice later?
    city = models.CharField(max_length=100, blank=True, default='')
    # dropdown?
    country = models.CharField(max_length=100, default='', blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def __str__(self):
        return f'{self.user}'

    def save(self, *args, **kwargs):
        self.slug = self.user.username
        super().save(*args, **kwargs)
