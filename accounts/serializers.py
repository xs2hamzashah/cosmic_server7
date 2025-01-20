from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import UserProfile, CustomUser, Company
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError, ValidationError


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'full_name', 'phone_number', 'username', 'password', 'confirm_password', 'phone_number']

    def validate(self, data):
        # Restrict updating the email field
        if self.instance:  # self.instance will be set only when updating, not during creation
            if 'email' in data or 'username' in data:
                raise serializers.ValidationError("Updating the email or username is not allowed.")
        # Check for password and confirm_password only if they are being updated
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if 'password' in data or 'confirm_password' in data:
            if password != confirm_password:
                raise serializers.ValidationError("Passwords do not match.")
            try:
                validate_password(password)
            except DjangoValidationError as e:
                raise DRFValidationError({"password": e.messages})

        return data


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'phone_number', 'description', 'city']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    company = CompanySerializer(allow_null=True)  # Allow null for non-sellers
    buyers_count = serializers.SerializerMethodField()
    packages_count = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'role', 'company', 'buyers_count', 'packages_count']

    def get_buyers_count(self, obj):
        if obj.role == UserProfile.Role.SELLER:
            # Count unique whatsapp numbers who have interacted with any of the seller's solutions
            return obj.solar_solutions.filter(
                interactions__isnull=False
            ).values('interactions__whatsapp_number').distinct().count()
        return 0

    def get_packages_count(self, obj):
        if obj.role == UserProfile.Role.SELLER:
            # Count all solar solutions for this seller
            return obj.solar_solutions.count()
        return 0

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
        if profile.role == 'seller':
            if not company_data:
                raise ValidationError(f"A company is required for sellers.")
            company_name = company_data.get('name')
            if company_name and Company.objects.filter(name=company_name).exists():
                raise ValidationError(f"A company with the name '{company_name}' already exists.")

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


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['role'] = self.user.userprofile.role
        return data