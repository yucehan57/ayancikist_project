from django.shortcuts import render, get_object_or_404
from userprofile.models import UserProfile

def index(request, slug):
    # pass 'slug' field for 'User' model above after customizing
    # the model. Then grab the user:
    # user = get_object_or_404(User, slug=slug)
    # user.posts will list user's posts in profile page
    # (notice that posts is a field attribute in 'user' ForeignKey
    # field in blog.models 'Post'

    # In a new tab ('see my comments') -> user.comments
    # to do above, have a related_name='comments' field attribute
    # ready in Comment model for a relation betweel two models.

    # A button will show all posts (pagination required?).
    # unless it is clicked, user will be displayed latest three posts

    # navbar 'logged in as {{}}' should be modified.
    userprofile = get_object_or_404(UserProfile, slug=slug)
    # Query user's posts
    latest_three_posts = userprofile.user.posts.all()[:3]
    all_posts = userprofile.user.posts.all()
    context = {
        'all_posts': all_posts,
        'latest_three_posts': latest_three_posts,
        'user': userprofile,
    }
    return render(request, 'userprofile/userprofile.html', context)
