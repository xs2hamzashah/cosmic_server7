from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, CustomUser


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    phone_number = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'full_name', 'phone_number', 'username', 'password', 'confirm_password', 'phone_number']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ['user', 'role', ]

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = user_data.pop('password')
        user_data.pop('confirm_password')

        user = CustomUser.objects.create(**user_data)
        user.set_password(password)  # Hash the password before saving
        user.save()

        profile = UserProfile.objects.create(user=user, **validated_data)
        return profile
