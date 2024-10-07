from rest_framework import serializers

from operations.models import Approval


class ApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Approval
        fields = ['admin_verified', 'discrepancy', 'discrepancy_resolved', 'email_notification_sent']
