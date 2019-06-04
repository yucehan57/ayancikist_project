from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages, auth
from blog.models import Post
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .forms import UserProfileForm

def register(request):
    # Right now user registration forms is created on the front-end
    # register.html by using labels and inputs corresponding for
    # those labels. This could be changed to user
    # UserCreationForm in 'accounts.forms'.
    if request.method == 'POST':
        # Get values from the registration form
        # (front-end data collection)
        # request.POST['first_name'] is:
        # 'first_name' corresponds to an input name
        # which also has a label on register.html
        # we grab that data and assign data that is grabbed with
        # POST request to 'first_name' variable name
        first_name  =   request.POST['first_name']
        last_name   =   request.POST['last_name']
        username    =   request.POST['username']
        email       =   request.POST['email']
        password    =   request.POST['password']
        password2   =   request.POST['password2']

        # we pass in values from request.POST (which is a dictionary)
        # to populate the UserProfileForm.
        user_profile_form = UserProfileForm(request.POST)

        # Check if passwords match
        if password == password2:
            # Check if username is already registered
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken')
                return redirect('register')
            else:
                # Everything looks good
                user = User.objects.create_user(username=username,
                                                password=password,
                                                email=email,
                                                first_name=first_name,
                                                last_name=last_name)

                # Save user
                user.save()
                messages.success(request, 'You are now registered')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')

def login(request):
    if request.method == 'POST':
        # Login Logic
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('blog-view')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('register')
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    return redirect('blog-view')

def profile(request, user_id):
    # pass 'slug' field for 'User' model above after customizing
    # the model. Then grab the user:
    # user = get_object_or_404(User, slug=slug)
    # user.posts will list user's posts in profile page
    # (notice that posts is a field attribute in 'user' ForeignKey
    # field in blog.models 'Post'

    # In a new tab ('see my comments') -> user.comments
    # to do above, have a related_name='comments' field attribute
    # ready in Comment model for a relation betweel two models.

    # navbar 'logged in as {{}}' should be modified.
    user = get_object_or_404(User, id=user_id)
    # Query user's posts
    posts = user.posts.all()

    context = {
        'posts': posts,
        'user': user,
    }
    return render(request, 'accounts/profile.html', context)
