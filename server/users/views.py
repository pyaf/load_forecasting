from django.shortcuts import render, render_to_response, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from users.models import *


def FormView(request):
    template_name = 'form.html'
    return render(request, template_name)

def LoginView(request):
    if request.user.is_authenticated:
        return redirect('/')

    template_name = 'form.html'
    if request.method == "POST":
        post = request.POST
        email = post.get('email')
        password = post.get('password')
        print(email, password)
        user = authenticate(username=email, email=email,     password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Invalid Credentials', fail_silently=True)
            return render(request, template_name, {})
    else:
        return render(request, template_name, {})


def RegistrationView(request):
    if request.user.is_authenticated:
        return redirect('/')
    template_name = 'form.html'
    if request.method == "POST":
        post = request.POST
        email = post.get('email')
        user, created = User.objects.get_or_create(username=email)
        if created:#create new User instance.
            user.email = email
            user.first_name = post.get('first-name')
            user.last_name = post.get('last-name')
            password = post.get('password')
            user.set_password(password)
            user.save()
            userprofile = UserProfile.objects.create(user=user)
            userprofile.college = post.get('college')
            userprofile.save()
            user = authenticate(username = email, password = password)
            login(request, user)
            return redirect('/')
        else:# already a user.
            messages.warning(request, "email already registered!, please try logging in.", fail_silently=True)
            return render(request, template_name)
    else:
        return render(request, template_name)

def LogoutView(request):
    logout(request) 
    return redirect('/')