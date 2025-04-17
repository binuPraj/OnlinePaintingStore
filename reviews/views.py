from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactMessage
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

def contactus(request):
    if request.method == 'POST':
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            
            # Get the form data from the AJAX request
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')
            email = request.POST.get('email', '')
            phone = request.POST.get('phone', '')
            message = request.POST.get('message', '')

            # Ensure that required fields are not empty
            if not first_name or not last_name or not email or not message:
                return JsonResponse({'success': False, 'message': 'All fields are required.'}, status=400)
            
            # Create and save the contact message
            try:
                contact_message = ContactMessage.objects.create(

                    phone=phone,
                    message=message,
                    user=request.user if request.user.is_authenticated else None  
                )
                print(f"Contact Message created: {contact_message}")
                send_mail(
                    subject=f'New Contact Message from {first_name} {last_name}',
                    message=f'Name: {first_name} {last_name}\nEmail: {email}\nPhone: {phone}\n\nMessage:\n{message}',
                    from_email=email,
                    recipient_list=[settings.ADMIN_EMAIL],
                    fail_silently=False,
                )

                return JsonResponse({
                    'success': True, 
                    'message': 'Message sent successfully. Thank you for your message!',
                    'contact_message': {
                        'phone': contact_message.phone,
                        'message': contact_message.message
                    }
                }, status=200)

            except Exception as e:
                return JsonResponse({'success': False, 'message': f'Error: {str(e)}'}, status=500)

        else:
            return JsonResponse({'success': False, 'message': 'Invalid request type.'}, status=400)

    return render(request, 'contact.html', {'user': request.user})

@login_required
def contact(request):
    return render(request, 'base/contact.html')

@login_required
def contact(request):
    return render(request,'base/contact.html')

def aboutus(request):
    return render(request,'base/aboutus.html')

def feedback(request):
    return render(request,'base/feedback.html')
