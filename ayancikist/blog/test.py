class Post(models.Model):
    slug = models.SlugField(unique=True)
    """
    """
    """
    """
    ### Say there is an object, an instance of Post model, with a title
    ### named 'how to write a blog'. Slug would be 'how-to-write-a-blog' after
    ### using slugify
    ### import slugify
    ### write a custom method to prevent above issue
    ### def _get_unique_slug(self):
    ###     slug = slugify(self.title)
    ###     unique_slug = slug
    ###     num = 1
    ###     while Post.objects.filter(slug=unique_slug).exists():
    ###         unique_slug = "{}-{}".format(slug, num)
    ###     return unique_slug
    ###
    ### def save(*args, **kwargs):
    ###     self.slug = unique_slug
    ###
    ###
