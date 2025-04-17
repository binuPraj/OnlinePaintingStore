
from django.shortcuts import redirect
from django.conf import settings


#if not authenticated login pagema lane
#Authenticated users only
def auth(view_function):
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  
        return view_function(request, *args, **kwargs)
    return wrapped_view

#if authenticated logout pagema pathaune
# **********Guest*********
# Guests only (unauthenticated users)
def guest(view_function):
    def wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('logout')  
        return view_function(request, *args, **kwargs)
    return wrapped_view

#cookie for user section
# class CustomSessionCookieMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         # Dynamically set the session cookie name based on the request path
#         if request.path.startswith('/admin/'):
#             settings.SESSION_COOKIE_NAME = 'admin_session'
#         else:
#             settings.SESSION_COOKIE_NAME = 'user_session'

#         # Get the response from the next middleware/view
#         response = self.get_response(request)

#         # Return the response object
#         return response

class CustomSessionCookieMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Dynamically set session cookie name based on request path
        if request.path.startswith('/admin/'):
            settings.SESSION_COOKIE_NAME = 'admin_sessionid'  # Admin session cookie
        else:
            settings.SESSION_COOKIE_NAME = 'sessionid'  # Regular user session cookie

        # Get the response from the next middleware/view
        response = self.get_response(request)

        # Return the response object
        return response