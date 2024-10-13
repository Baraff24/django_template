from functools import wraps

from rest_framework import status
from rest_framework.response import Response

from allauth.account.models import EmailAddress

from app.accounts.constants import COMPLETE


#####################################################################################
# DECORATORS #
#####################################################################################

# Decorator to check if user is active
def is_active(view_func):
    """
    Decorator to check if the user is active, authenticated, and has a verified email.
    """

    @wraps(view_func)
    def decorator(request, *args, **kwargs):
        user = request.user

        # Check if the user is authenticated and active
        if not user.is_authenticated or not user.is_active:
            return Response({"Error": "Your account is not active or authenticated."},
                            status=status.HTTP_403_FORBIDDEN)

        # Check if the email is verified
        if not EmailAddress.objects.filter(user=user, verified=True).exists():
            return Response({"Error": "Your email is not verified."},
                            status=status.HTTP_403_FORBIDDEN)

        # Check if the user's data completion status is COMPLETE
        if user.status != COMPLETE:
            return Response({
                "Error": "You have to complete the data completion process",
                "userStatus": user.status
            }, status=status.HTTP_403_FORBIDDEN)

        # If all checks pass, proceed to the view
        return view_func(request, *args, **kwargs)

    return decorator
