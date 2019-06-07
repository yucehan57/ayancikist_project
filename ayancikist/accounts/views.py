from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages, auth
from blog.models import Post
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .forms import UserProfileForm, ExtendedUserCreationForm
from userprofile.models import UserProfile

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

# def register(request):
#     if request.method == 'POST':
#         form = ExtendedUserCreationForm(request.POST)
#         profile_form = UserProfileForm(request.POST)
#
#         if form.is_valid() and profile_form.is_valid():
#             # return a user from the form save
#             user = form.save()
#             # we pass 'commit=False' to not save the profile
#             # that we create using the profile_form to the database
#             # right away
#             profile = profile_form.save(commit=False)
#             # There is a 'OneToOneField' relation with the profile user
#             # and user instance of User model (defined in userprofile.models)
#             # since UserCreationForm and UserProfileForm are two different
#             # forms, we define who the user is for UserProfile model.
#             profile.user = user
#             profile.save()
#
#             username = form.cleaned_data.get['username']
#             password = form.cleaned_data.get['password']
#             # built-in authentication (from django.contrib import auth)
#             user = auth.authenticate(username=username, password=password)
#             # Automatically login registered user with built-in Login
#             # Uncomment the following line if that's what you want:
#             auth.login(request, user)
#             return redirect('blog-view')
#     else:
#         # Serve empty form as long as it is a 'GET' request
#         form = ExtendedUserCreationForm()
#         profile_form = UserProfileForm()
#
#     context = {
#         'form': form,
#         'profile_form': profile_form,
#     }
#     return render(request, 'accounts/register.html', context)

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

def profile(request, slug):
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
    userprofile = get_object_or_404(UserProfile, slug=slug)
    # Query user's posts
    posts = userprofile.user.posts.all()

    context = {
        'posts': posts,
        'user': userprofile,
    }
    return render(request, 'accounts/profile.html', context)
