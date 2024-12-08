from rest_framework import serializers

from accounts.models import UserProfile
from accounts.serializers import UserProfileSerializer
from pricelist.models import Panel
from pricing.models import SubscriptionPlan


class PanelSerializer(serializers.ModelSerializer):
    seller = UserProfileSerializer(read_only=True)

    class Meta:
        model = Panel
        fields = ["id" ,"seller","brand_name","specification","capacity","unit","price"]
