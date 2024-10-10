from rest_framework import serializers

from listings.models import SolarSolution
from operations.models import Approval


class ApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Approval
        fields = ['admin_verified', 'discrepancy', 'discrepancy_resolved', 'email_notification_sent']


class SendOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15, required=True)


class ConfirmOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15, required=True)
    otp_code = serializers.CharField(max_length=6, required=True)
    solar_solution_id = serializers.PrimaryKeyRelatedField(queryset=SolarSolution.objects.all(), required=False)

