from rest_framework import viewsets, status

from rest_framework.response import Response
from rest_framework.decorators import action

from accounts.permissions import IsAdmin
from core.utils import send_approval_notification
from operations.models import Approval
from operations.serializers import ApprovalSerializer


class ApprovalViewSet(viewsets.ModelViewSet):
    queryset = Approval.objects.all()
    serializer_class = ApprovalSerializer
    permission_classes = [IsAdmin]  # Restrict access to admins

    @action(detail=False, methods=['GET'])
    def pending(self, request):
        pending_approvals = Approval.objects.filter(admin_verified=False)
        serializer = self.get_serializer(pending_approvals, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['POST'])
    def approve(self, request, pk=None):
        approval = self.get_object()
        serializer = self.get_serializer(approval, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(admin_verified=True, email_notification_sent=True)
            # Call function to send email
            # In future we'll make this async...
            send_approval_notification(approval.solution.seller)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
