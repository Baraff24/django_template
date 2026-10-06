from allauth.account.models import EmailAddress
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission

from .constants import COMPLETE


class IsActiveAndVerified(BasePermission):
    """
    Permission class that checks if the user is authenticated, active,
    has a verified email.
    """

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated or not user.is_active:
            # Return a PermissionDenied exception if the user is not authenticated or active
            raise PermissionDenied("Your account is not active or authenticated.")

        if not EmailAddress.objects.filter(user=user, verified=True).exists():
            # Return a PermissionDenied exception if the user's email is not verified
            raise PermissionDenied("Your email is not verified.")

        return True


class IsActiveAndVerifiedAndComplete(IsActiveAndVerified):
    """Require a verified, active account with a completed profile."""

    def has_permission(self, request, view):
        super().has_permission(request, view)
        if request.user.status != COMPLETE:
            # Return a PermissionDenied exception if the user's status is not COMPLETE
            raise PermissionDenied(
                f"You have to complete the data completion process. Current status: {request.user.status}"
            )

        return True


class IsSuperuserOrSelf(BasePermission):
    """
    Allows access only if the user is superuser or the owner of the object.
    """

    def has_object_permission(self, request, view, obj):
        # obj is a User instance in our case
        return request.user.is_superuser or request.user.id == obj.id
