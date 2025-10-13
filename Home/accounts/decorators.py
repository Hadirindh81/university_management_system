# account decorator 
from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

def _get_role(user):
    try:
        role = getattr(user, 'profile', None) and getattr(user.profile, 'role', None)
        if role:
            return str(role).lower()
    except Exception:
        pass
    return None

def role_required(allowed_roles):
    """
    Decorator for function views.
    allowed_roles: list/tuple of strings, case-insensitive e.g. ['admin','teacher']
    """
    allowed = [r.lower() for r in allowed_roles]

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect(f"{reverse('login')}?next={request.path}")
            role = _get_role(request.user)
            if role in allowed:
                return view_func(request, *args, **kwargs)
            messages.error(request, "You don't have permission to access that page.")
            return redirect('home')
        return _wrapped
    return decorator
