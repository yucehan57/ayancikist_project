from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify

class Post(models.Model):
    # related_name above achieves the following:
    # {{user.posts.count}} would show how many posts the user has.
    # related_name='posts' allows user model to have access to post model
    # standard name given to 'related_name' attribute is the plural of the model
    # we are in. i.e. 'posts' or 'comments' as will be seen below.
    user            = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title           = models.CharField(max_length=200)
    slug            = models.SlugField(unique=True, allow_unicode=True)
    text            = models.TextField()
    published_date  = models.DateTimeField(auto_now=True)

    def summary(self):
        """Return a summary for very long posts to
        get a glimpse from admin panel"""
        return self.text[:100]

    def save(self, *args, **kwargs):
        # Automatically assign slug using title field
        # by overriding save method
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def pub_date_pretty(self):
        return self.published_date.strftime('%b %e, %Y')

    def __str__(self):
        """String representation"""
        return self.title

    def get_absolute_url(self):
        # what does kwargs={'slug':self.slug} really achieve here?
        # where would we use 'key-value' pair?
        """Returns the url to access a detailed post"""
        return reverse('post-detail', kwargs={"slug": self.slug})

    class Meta:
        ordering = ['-published_date',]


class Comment(models.Model):
    # related_name='comments' gives you access to comment model from post model
    # {{ post.comments.count }} gives you number of comments for a given post
    # This is done by giving a "related_name='comments'" attribute to ForeignKey
    # (field name that is named after the model to be given access to)
    # with whichever model you want to give access to
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
