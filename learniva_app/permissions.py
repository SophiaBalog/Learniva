from functools import wraps
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied


def is_teacher(user):
    return user.is_authenticated and (
        user.is_superuser or user.groups.filter(name='Teachers').exists()
    )


def teacher_required(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())  # не увійшов → на сторінку входу
        if not is_teacher(request.user):
            raise PermissionDenied                              # учень → помилка 403
        return view(request, *args, **kwargs)
    return wrapper