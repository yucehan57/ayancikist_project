### field_values=Post._meta.get_fields()
### for fv in field_values:
###     print(fv)
### -> above will return all the fields available in our Post model

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
    slug            = models.SlugField(unique=True)
    text            = models.TextField()
    published_date  = models.DateTimeField(auto_now=True)
    # pip install Pillow
    image           = models.ImageField(null=True, blank=True,
                                        upload_to='photos/%Y/%m/%d/',)


    def summary(self):
        """Return a summary for very long posts to
        get a glimpse from admin panel"""
        return self.text[:100]

    def approved_comments(self):
        # query only approved comments
        return self.comments.filter(approved_comment=True)

    def _get_unique_slug(self):
        """Assigns a number to the end of a given slug field to prevent
        duplicated slug error. if title of a post is 'ayancik', and another
        user creates another post with the same title, second posts' slug
        is assigned a value: 'ayancik-2'"""
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        """Automatically assign slug to objects
        by overriding save method"""
        self.slug = self._get_unique_slug()
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
    # slug                = models.SlugField(unique=True, null=True, blank=True)
    # image               = models.ImageField(null=True, blank=True,
    #                                         upload_to='photos/%Y/%m/%d/',)

    # """Is slugifying comment text necessary?"""
    # def _get_unique_slug(self):
    #     # Since slug is derived from comment's first 15 characters,
    #     # there may, though unlikey, two comments that start with
    #     # same characters. To prevent duplicate slug values in two seperate
    #     # comment objects, we need to define a method to create unique
    #     # slug fields for different comment instances.
    #     slug = slugify(self.text)[:15]
    #     unique_slug = slug
    #     num = 0
    #     while Comment.objects.filter(slug=unique_slug).exists:
    #         unique_slug = "{}-{}".format(slug, num)
    #         num += 1
    #         return unique_slug
    #
    # def save(self, *args, **kwargs):
    #     # Override same method to assign unique slug fields to every different
    #     # comment object
    #     self.slug = self._get_unique_slug()
    #     super().save(*args, **kwargs)

    def approve_comment(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text
