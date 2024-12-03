from rest_framework import serializers

from accounts.models import UserProfile, CustomUser
from .models import SubscriptionPlan, SubscriptionPass


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = ['id', 'name', 'description', 'price']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be a positive number.")
        return value


class SubscriptionPlanDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = ['id', 'name', 'price']


class SubscriptionPassUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'full_name', 'email']


class SubscriptionPassUserProfileSerializer(serializers.ModelSerializer):
    user = SubscriptionPassUserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'role',]


class SubscriptionPassSerializer(serializers.ModelSerializer):
    seller = SubscriptionPassUserProfileSerializer(read_only=True)
    plan = SubscriptionPlanDetailSerializer(read_only=True)

    class Meta:
        model = SubscriptionPass
        fields = ['id', 'seller', 'plan', 'created']
