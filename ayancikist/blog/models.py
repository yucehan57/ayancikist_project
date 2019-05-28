from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    title           = models.CharField(max_length=200)
    slug            = models.SlugField()
    text            = models.TextField()
    published_date  = models.DateTimeField(auto_now=True)

    def summary(self):
        """Return a summary for very long posts to
        get a glimpse from admin panel"""
        return self.text[:100]

    def pub_date_pretty(self):
        return self.published_date.strftime('%b %e, %Y')

    def __str__(self):
        """String representation"""
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a detailed post"""
        return reverse('post-detail', kwargs={"slug": self.slug})

    class Meta:
        ordering = ['-published_date']


class Comment(models.Model):
    post                = models.ForeignKey('blog.Post', on_delete=models.CASCADE,
                             related_name='comments')
    user                = models.CharField(max_length=200)
    text                = models.TextField()
    created_date        = models.DateTimeField(default=timezone.now)
    approved_comment    = models.BooleanField(default=False)

    def approve_comment(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text
