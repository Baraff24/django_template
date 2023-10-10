from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CompleteProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'telephone', 'gender',
                  'age', 'nationality', 'domicile', 'education',
                  'university', 'occupation', 'socio_economic_status',
                  'self_harmful_thoughts', 'n_exercises', 'n_daily_questions', 'n_baseline']
