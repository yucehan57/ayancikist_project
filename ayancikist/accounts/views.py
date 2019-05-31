from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages, auth
from blog.models import Post
from django.shortcuts import get_object_or_404

def register(request):
    if request.method == 'POST':
        # Get values from the registration form
        first_name  =   request.POST['first_name']
        last_name   =   request.POST['last_name']
        username    =   request.POST['username']
        email       =   request.POST['email']
        password    =   request.POST['password']
        password2   =   request.POST['password2']

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

def profile(request):
    # pass 'slug' field for 'User' model above after customizing
    # the model. Then grab the user:
    # user = get_object_or_404(User, slug=slug)
    # user.posts will list user's posts in profile page
    # (notice that posts is a field attribute in 'user' ForeignKey
    # field in blog.models 'Post'

    # In a new tab ('see my comments') -> user.comments
    # to do above, have a related_name='comments' field attribute
    # ready in Comment model for a relation betweel two models.
    context = {

    }
    return render(request, 'accounts/profile.html', context)
