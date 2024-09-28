from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Accept nested user data

    class Meta:
        model = UserProfile
        fields = ['user', 'role']

    def create(self, validated_data):
        user_data = validated_data.pop('user')

        user = User.objects.create(**user_data)
        profile = UserProfile.objects.create(user=user, **validated_data)
        return profile
