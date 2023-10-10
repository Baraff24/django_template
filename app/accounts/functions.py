from functools import wraps

from rest_framework import status
from rest_framework.response import Response

from allauth.account.models import EmailAddress


#####################################################################################
# DECORATORS #
#####################################################################################

# Decorator to check if user is active
def is_active(view_func):
    @wraps(view_func)
    def decorator(request, *args, **kwargs):
        user = request.user
        if user.is_active and user.is_authenticated:
            if EmailAddress.objects.filter(user=user, verified=True):
                return view_func(request, *args, **kwargs)
            else:
                return Response({"Error": "Your email is not verified"},
                                status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"Error": "Your account is not active"},
                            status=status.HTTP_403_FORBIDDEN)

    return decorator
