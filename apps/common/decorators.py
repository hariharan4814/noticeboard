from functools import wraps

from django.core.exceptions import PermissionDenied


def staff_or_superuser_required(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return view_func(request, *args, **kwargs)

        if request.user.is_staff or request.user.is_superuser:
            return view_func(request, *args, **kwargs)

        raise PermissionDenied

    return wrapped_view