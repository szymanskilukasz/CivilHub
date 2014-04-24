# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.contrib.auth.models import User
from models import UserProfile
from forms import *

def index(request):
    """
    User profile / settings
    """
    from forms import UserProfileForm
    if not request.user.is_authenticated():
        return redirect('user:login')
    user = User.objects.get(pk=request.user.id)
    try:
        prof = UserProfile.objects.get(user=user.id)
    except:
        prof = UserProfile()
        prof.user = user
        prof.save()
    ctx = {
        'user': user,
        'profile': prof,
        'form': UserProfileForm(initial={
                  'username':   user.username,
                  'first_name': user.first_name,
                  'last_name':  user.last_name,
                  'email':      user.email
              }),
        'avatar_form': AvatarUploadForm(),
        'title': 'User Area',
    }
    return render(request, 'userspace/index.html', ctx)

def register(request):
    """
    Register new user via django system
    """
    if request.method == 'POST':
        f = RegisterForm(request.POST)
        if f.is_valid():
            user = User()
            username = f.cleaned_data['username']
            password = f.cleaned_data['password']
            user.username = username
            user.set_password(password)
            user.save()
            # Re-fetch user object from DB
            user = User.objects.latest('id')
            # Create user profile
            prof = UserProfile()
            prof.user = user
            prof.save()
            user = auth.authenticate(username = username, password = password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    return redirect('user:index')
        else:
            return redirect(reverse('user:register'))
    ctx = {
        'form': RegisterForm,
        'title': 'Sign Up',
    }
    return render(request, 'userspace/register.html', ctx)

def passet(request):
    """
    Set credentials for new users registered with social auth
    """
    ctx = {
        'title': "Set your password",
    }
    if request.method == 'POST':
        f = RegisterForm(request.POST)
        if f.is_valid():
            user = User(request.user.id)
            user.username = f.cleaned_data['username']
            user.set_password(f.cleaned_data['password'])
            user.save()
            # Re-fetch user object from DB
            user = User.objects.get(pk=request.user.id)
            # Create user profile if not exists
            try:
                prof = UserProfile.objects.get(user=request.user.id)
            except:
                prof = UserProfile()
                prof.user = user
                prof.save()
            return redirect('user:index')
    ctx['form'] = RegisterForm()
    return render(request, 'userspace/pass.html', ctx)

def login(request):
    """
    Login form
    """
    if request.user.is_authenticated():
        return redirect('user:index')
    if request.method == 'POST':
        f = LoginForm(request.POST)
        if f.is_valid():
            username = f.cleaned_data['username']
            password = request.POST['password']
            user = auth.authenticate(username = username, password = password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    return redirect('user:index')
        else:
            return redirect(reverse('user:login'))
    f = LoginForm()
    ctx = {
        'title': 'Login',
        'form': f,
    }
    return render(request, 'userspace/login.html', ctx)

def logout(request):
    """
    Logout currently logged in user
    """
    auth.logout(request)
    return redirect('user:login')

def save_settings(request):
    """
    Save changes made by user in his/her profile
    """
    if request.method == 'POST':
        user = User.objects.get(pk=request.user.id)
        f = UserProfileForm(request.POST)
        if f.is_valid():
            user.first_name = f.cleaned_data['first_name']
            user.last_name  = f.cleaned_data['last_name']
            user.email      = f.cleaned_data['email']
            error = None
            if user.email and User.objects.filter(email=user.email).exclude(pk=user.id).exists():
                error = "This email is already used"
            if error != None:
                return HttpResponse('Form invalid')
            user.save()
            return redirect('user:index')
    return HttpResponse('Form invalid')

def chpass(request):
    """
    Change user's password
    """
    if request.method == 'POST':
        f = PasswordResetForm(request.POST)
        if f.is_valid():
            current = f.cleaned_data['current']
            password = f.cleaned_data['password']
            user = User.objects.get(pk=request.user.id)
            username = user.username
            chk = auth.authenticate(username = username, password = current)
            if chk is not None:
                if chk.is_active:
                    user.set_password(password)
                    user.save()
                    return redirect('user:index')
            else:
                return HttpResponse('Your password is invalid. Login again')
        else:
            return HttpResponse('Form invalid')
    f = PasswordResetForm()
    ctx = {
        'title': 'Change password',
        'form': f,
    }
    return render(request, 'userspace/chpass.html', ctx)

def upload_avatar(request):
    """
    Upload/change user avatar
    """
    if request.method == 'POST':
        f = AvatarUploadForm(request.POST, request.FILES)
        if f.is_valid():
            user = UserProfile.objects.get(user=request.user.id)
            user.avatar = request.FILES['avatar']
            user.save()
    return redirect('user:index')
