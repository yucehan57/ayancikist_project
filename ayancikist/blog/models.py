from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

from django.contrib.auth import get_user_model
User = get_user_model()

class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    published_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        """String representation"""
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a detailed post"""
        return reverse('post-detail', kwargs={"pk": self.pk})

    class Meta:
        ordering = ['-published_date']
        unique_together = ('user',)
