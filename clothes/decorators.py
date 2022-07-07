from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('clothes:admin_view')
        else:

            return view_func(request, *args, **kwargs)
    return wrapper_func

def allow_users(allowed_roled=[]):
    def decorator(view_func):
        def wrapped_func(request, *args, **kwargs):
            print("working", allowed_roled)
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roled:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('clothes:home')
        return wrapped_func
    return decorator