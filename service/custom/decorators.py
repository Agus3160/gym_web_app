from django.shortcuts import redirect
from django.urls import reverse
from functools import wraps
from ..models import ClientInfo

def redirect_to_home_if_logged_in(view_func, destiny='home'):
    """
    Custom decorator to redirect users to the home page if they are already logged in.
    """
    def wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            # Redirect to the home page
            return redirect(destiny) 
        else:
            # Call the original view function if the user is not logged in
            return view_func(request, *args, **kwargs)
    return wrapped_view



def client_profile_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Check if the user is logged in
        if not request.user.is_authenticated:
            return redirect(reverse('sign-in'))  # Redirect to login page if not logged in
        
        # Check if the user has a client profile
        if not ClientInfo.objects.filter(user_id=request.user.id).exists():
            return redirect(reverse('sign-up-client'))  # Redirect to create client profile page
        
        # If the user has a client profile, allow access to the view
        return view_func(request, *args, **kwargs)
    return wrapper