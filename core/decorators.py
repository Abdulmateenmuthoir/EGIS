from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import redirect


def admin_required(view_func):
    """Decorator that restricts access to admin users only."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('core:login')
        if not request.user.is_admin:
            return HttpResponseForbidden(
                '<h1>403 Forbidden</h1>'
                '<p>You do not have permission to access this page.</p>'
            )
        return view_func(request, *args, **kwargs)
    return _wrapped_view
