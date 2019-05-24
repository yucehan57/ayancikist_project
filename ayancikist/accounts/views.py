from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

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
