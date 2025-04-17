from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site

from .form import CustomUserCreationForm
from .models import Profile
from store.middlewares import auth, guest

import requests
import logging

#for email verification
import requests
from django.http import JsonResponse

from .models import *           #euta euta garna naparos vanerw ailelai sabai tables import

import logging

def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)
        
        # Debugging log
        logging.debug(f'Activating user {user.username}, token valid: {default_token_generator.check_token(user, token)}')

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()

            Profile.objects.create(user=user)
            profile, created = Profile.objects.get_or_create(user=user)
            profile.is_email_verified = True
            profile.save()

            messages.success(request, "Your account has been activated. You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Activation link is invalid or has expired.")
            return redirect('login')

    except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        # Log the exception details
        logging.error(f'Error during activation: {e}')
        messages.error(request, "Invalid activation link.")
        return redirect('login')
    
def send_activation_email(user,request):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(str(user.pk).encode())

    current_site = get_current_site(request)
    activation_link = f"{current_site}/accounts/activate/{uid}/{token}/"

    # Send the email
    email_subject = 'Activate your account'
    email_body = render_to_string('accounts/activation_email.html', {
        'user': user,
        'activation_link': activation_link
    })
    send_mail(email_subject, email_body, 'unxaun@example.com', [user.email])

def verify_email_with_hunter(email):
    api_key = '332a23750c6181cbe4fa87228b4585cfcb2f33ed'  # Replace with your Hunter.io API key
    url = 'https://api.hunter.io/v2/email-verifier'
    
    params = {
        'email': email,
        'api_key': api_key,
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise exception for HTTP errors

        data = response.json()
        print(f"API Response for {email}: {data}")  # Debugging: Print the full response

        result = data.get('data', {}).get('result')
        if result == 'deliverable' or result == 'risky':
            return True  # Accept deliverable and risky emails
        else:
            print(f"Email {email} is {result}.")
            return False  # Invalid email
    except requests.exceptions.RequestException as e:
        print(f"Error verifying email: {e}")
        return False

@guest
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        # Verify email using Hunter.io API
        if not verify_email_with_hunter(request.POST.get('email')):
            messages.warning(request, "The email address is invalid or not deliverable.")
            return HttpResponseRedirect(request.path_info)

        # Validate the form
        if form.is_valid():
            user = form.save(commit=False)  
            user.is_active = False
            user.save()

            # Send email activation link
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(str(user.pk).encode()) 

            # Get current domain
            current_site = get_current_site(request)
            domain = current_site.domain
            activation_url = f'http://{domain}/accounts/activate/{uid}/{token}/'

            send_mail(
                'Activate your account',
                f'Click the link to activate your account: {activation_url}',
                'from@example.com',  
                [user.email],
                fail_silently=False,
            )

            messages.success(request, "Registration successful! An activation email has been sent.")
            return redirect('login')  # Redirect to login page
        else:
            messages.error(request, "Form submission failed.")

    else:
        initial_data = {'username': '', 'password1': '', 'password2':'', 'first_name' :'','last_name':'', 'email':''}
        form = CustomUserCreationForm(initial=initial_data)

    return render(request, 'accounts/register.html', {'form': form})

@guest
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()

            if user.is_active:
                login(request, user)
                return redirect(request.POST.get('next', 'home'))
            else:
                messages.error(request, "Your account is not activated. Please check your email.")
                return redirect('login') 
        else:
            messages.error(request, "Invalid username or password.")
    else:
        initial_data = {'username': '', 'password': ''}
        form = AuthenticationForm(initial=initial_data)
        if 'next' in request.GET:
            messages.info(request, "Please log in to access the requested page.")
    
    
    return render(request, 'accounts/login.html', {'form': form})
@auth
def logout_page(request):
    """Renders the logout confirmation page."""
    return render(request, "accounts/logout.html")

@auth
def logout_confirm(request):
    """Logs the user out and redirects to the login page."""
    logout(request)
    return redirect('login')                  #for logout to work
 

 