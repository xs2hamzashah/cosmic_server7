from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, CustomUser, Company


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


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name', 'phone_number', 'description', 'city']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    company = CompanySerializer(allow_null=True)  # Allow null for non-sellers

    class Meta:
        model = UserProfile
        fields = ['user', 'role', 'company']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = user_data.pop('password')
        user_data.pop('confirm_password')

        company_data = validated_data.pop('company', None)

        user = CustomUser.objects.create(**user_data)
        user.set_password(password)  # Hash the password before saving
        user.save()

        # Create a company only if the user is a seller
        profile = UserProfile.objects.create(user=user, **validated_data)
        if profile.role == 'seller' and company_data:
            company = Company.objects.create(owner=profile, **company_data)
            profile.company = company
            profile.save()

        return profile


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate_new_password(self, value):
        # Add any password validation logic if needed
        return value
