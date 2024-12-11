from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    A general serializer for the User model.
    """

    class Meta:
        model = User
        fields = '__all__'


class CompleteProfileSerializer(serializers.ModelSerializer):
    """
    Serializer used for profile completion.
    Only includes fields required to complete the profile.
    """

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'telephone', 'gender']
        extra_kwargs = {
            'first_name': {'required': True, 'allow_blank': False},
            'last_name': {'required': True, 'allow_blank': False},
            'telephone': {'required': True, 'allow_blank': False},
            'gender': {'required': True, 'allow_blank': False}
        }

    def update(self, instance, validated_data):
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.telephone = validated_data['telephone']
        instance.gender = validated_data['gender']
        instance.save()
        return instance
