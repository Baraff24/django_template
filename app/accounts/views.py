from rest_framework import status, generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .constants import PENDING_COMPLETE_DATA, COMPLETE
from .models import User
from .serializers import UserSerializer, CompleteProfileSerializer
from .permissions import IsActiveAndVerifiedAndComplete, IsSuperuserOrSelf


class UsersListAPI(generics.ListAPIView):
    """
    Return a list of all users.
    Only superusers can access this endpoint.
    """
    permission_classes = [IsAuthenticated, IsActiveAndVerifiedAndComplete]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def list(self, request, *args, **kwargs):
        # Check if the user is superuser, otherwise deny access
        if not request.user.is_superuser:
            raise PermissionDenied("You do not have permission to view this resource.")
        return super().list(request, *args, **kwargs)


class UserDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a user instance.
    Only superusers or the user itself can perform these actions.
    When deleting, the user is set as inactive rather than being removed.
    """
    permission_classes = [IsAuthenticated, IsActiveAndVerifiedAndComplete, IsSuperuserOrSelf]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_destroy(self, instance):
        # Instead of deleting the user, set is_active to False
        instance.is_active = False
        instance.save()


class CompleteProfileAPI(generics.UpdateAPIView):
    """
    Allows a user with PENDING_COMPLETE_DATA status to complete their profile.
    Once completed, the user's status is set to COMPLETE.
    """
    permission_classes = [IsAuthenticated, IsActiveAndVerifiedAndComplete]
    serializer_class = CompleteProfileSerializer

    response_data = None

    def get_object(self):
        # The object is the authenticated user
        user = self.request.user
        if not isinstance(user, User):
            # If the user is not an instance of User, raise an error
            raise PermissionDenied("You do not have permission to complete this action.")

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        if user.status != PENDING_COMPLETE_DATA:
            # If the user's status is not PENDING_COMPLETE_DATA, raise an error
            return Response({"error": f"The user {user}, has already completed the profile."},
                            status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs)

    def perform_update(self, serializer):
        # Update user's data and set status to COMPLETE
        user = self.get_object()
        serializer.save()  # This will update the fields specified in the serializer
        user.status = COMPLETE
        user.save()
        # Returning a custom response
        self.response_data = {'user_status': COMPLETE}

    def put(self, request, *args, **kwargs):
        response = super().put(request, *args, **kwargs)
        # If we have a custom response_data, return it
        if hasattr(self, 'response_data'):
            return Response(self.response_data, status=status.HTTP_200_OK)
        return response
