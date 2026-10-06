from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    A general serializer for the User model.
    """

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "telephone",
            "gender",
            "status",
        ]
        read_only_fields = ["id", "email", "status"]


class CompleteProfileSerializer(serializers.ModelSerializer):
    """
    Serializer used for profile completion.
    Only includes fields required to complete the profile.
    """

    class Meta:
        model = User
        fields = ["first_name", "last_name", "telephone", "gender"]
        extra_kwargs = {
            "first_name": {"required": True, "allow_blank": False},
            "last_name": {"required": True, "allow_blank": False},
            "telephone": {"required": True, "allow_blank": False},
            "gender": {"required": True, "allow_blank": False},
        }
