from functools import wraps
from django.http import HttpResponseForbidden
from core.models import User


def is_authenticated_user(function):
    @wraps(function)
    def check_value(request, *args, **kwargs):
        user = User.objects.filter(id=request.user.id)
        if user.exists():
            return function(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()

    return check_value


def is_user_admin(function):
    @wraps(function)
    def check_value(request, *args, **kwargs):
        user = User.objects.filter(id=request.user.id)
        if user.exists() and user.is_superuser:
            return function(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()

    return check_value


def is_user_staff(function):
    @wraps(function)
    def check_value(request, *args, **kwargs):
        user = User.objects.filter(id=request.user.id)
        if user.exists() and user.is_staff:
            return function(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()

    return check_value
