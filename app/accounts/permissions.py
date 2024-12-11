from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from allauth.account.models import EmailAddress

from app.accounts.constants import COMPLETE


class IsActiveAndVerifiedAndComplete(BasePermission):
    """
    Permission class that checks if the user is authenticated, active,
    has a verified email, and that the user's status is COMPLETE.
    """

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated or not user.is_active:
            # Return a PermissionDenied exception if the user is not authenticated or active
            raise PermissionDenied("Your account is not active or authenticated.")

        if not EmailAddress.objects.filter(user=user, verified=True).exists():
            # Return a PermissionDenied exception if the user's email is not verified
            raise PermissionDenied("Your email is not verified.")

        if user.status != COMPLETE:
            # Return a PermissionDenied exception if the user's status is not COMPLETE
            raise PermissionDenied(f"You have to complete the data completion process. Current status: {user.status}")

        return True


class IsSuperuserOrSelf(BasePermission):
    """
    Allows access only if the user is superuser or the owner of the object.
    """

    def has_object_permission(self, request, view, obj):
        # obj is a User instance in our case
        return request.user.is_superuser or request.user.id == obj.id
