from django.db import models
from django.contrib import auth
from django.utils.text import slugify

class UserProfile(models.Model):
    # python manage.py shell
    #>User._meta.get_fields() shows all of the fields of User model
    # user = models.OneToOneField('auth.User')
    # we need slug field for profile page url direction and views

    def __str__(self):
        return "{}".format(self.username)
