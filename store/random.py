
def generate_activation_token(user):
    # Generate the token for the user
    token = default_token_generator.make_token(user)
    # URL-safe encoding of the user's ID to pass in the URL
    uid = urlsafe_base64_encode(str(user.pk).encode()).decode()
    return uid, token

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
        email = request.POST.get('email')

        # Verify email using Hunter.io API
        if not verify_email_with_hunter(email):
            messages.warning(request, "The email address is invalid or not deliverable.")
            return HttpResponseRedirect(request.path_info)

        # Check if email already exists in the database using the form validation
        if User.objects.filter(email=email).exists():
            messages.warning(request, "Email is already taken")
            return HttpResponseRedirect(request.path_info)

        if form.is_valid():
            user_obj = form.save(commit=False)
            user_obj.email = email
            user_obj.set_password(form.cleaned_data['password1'])
            user_obj.save()

            # Send verification email
            token = default_token_generator.make_token(user_obj)
            uid = urlsafe_base64_encode(str(user_obj.pk).encode()).decode()
            verification_link = f"{get_current_site(request).domain}/verify/{uid}/{token}/"

            subject = 'Activate Your Account'
            message = render_to_string('accounts/activation_email.html', {
                'user': user_obj,
                'verification_link': verification_link,
            })

            send_mail(subject, message, 'noreply@yourdomain.com', [user_obj.email])

            messages.success(request, "Registration successful! Please check your email to activate your account.")
            return redirect('login')

    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})