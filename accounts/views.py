from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .forms import UserRegisterForm
from .decorators import unauthenticated_user


# Restrict the authenticated user from visiting this page and redirect to home page. 
@unauthenticated_user
def user_register(request):
    """
    Create new user.
    """
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # fetch submitted data
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password1")
            # create new user
            new_user = User.objects.create(
                username = username,
                email = email,
            )
            new_user.set_password(password)
            new_user.save()
            # Display success message
            messages.success(request, f'New Account has been created for {username}.', extra_tags='register')
            return redirect('accounts:login')
    else:
        form = UserRegisterForm()    
    context = {'form':form}
    return render(request, 'accounts/register.html', context)

def validate_username(request):
    """
    Validate username asynchronously by ajax, and check if it's already been taken or not.
    """
    # get submitted username.
    username = request.GET.get('username', None)
    if request.user.username:
        # check if an account with this username already exists, in case of editing user's profile.
        is_username_taken = User.objects.filter(username__iexact=username).exclude(username__iexact=request.user.username).exists()
    else:
        # check if an account with this username already exists, in case of registering new user.
        is_username_taken = User.objects.filter(username__iexact=username).exists()
    data = {'is_username_taken':is_username_taken}
    if data['is_username_taken']:
        data['error_message'] = 'An account with this Username already exists.'
    return JsonResponse(data)

def validate_email(request):
    """
    Validate email asynchronously by ajax, and check if it's already been taken or not.
    """
    # get submitted email.
    email = request.GET.get('email', None)
    try:
        # check if an account with this email already exists, in case of editing user's profile.
        is_email_taken = User.objects.filter(email__iexact=email).exclude(email__iexact=request.user.email).exists()
    except:    
        # check if an account with this email already exists, in case of registering new user.
        is_email_taken = User.objects.filter(email__iexact=email).exists()
    data = {'is_email_taken':is_email_taken}
    if data['is_email_taken']:
        data['error_message'] = 'An account with this Email already exists.'
    return JsonResponse(data)

@unauthenticated_user
def user_login(request):
    """
    Login user.
    """
    if request.method == "POST":
        # fetch submitted data.
        username_email = request.POST.get("username_email")
        password = request.POST.get("password")
        # check if the entered username or email exists.
        user = authenticate(username=username_email, password=password)
        # Credentials are correct.
        if user:
            login(request, user)
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            else:
                return redirect('/') 
        else:
            # Display error message.
            messages.error(request, 'Username or Email is incorrect.', extra_tags='login')
    return render(request, 'accounts/login.html', {})

def user_logout(request):
    """
    Logout user.
    """
    logout(request)
    return redirect('accounts:login') 