from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    author          =   models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title           =   models.CharField(max_length=200)
    text            =   models.TextField()
    published_date  =   models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """String representation"""
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a detailed post"""
        return reverse('post-detail', args=[str(self.id)])
