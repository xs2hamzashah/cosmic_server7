import random

from django.core.cache import cache
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny

from rest_framework.response import Response
from rest_framework.decorators import action
from twilio.rest import Client

from accounts.permissions import IsAdmin
from core.utils import send_approval_notification
from cosmic_server7 import settings
from listings.models import BuyerInteraction
from operations.models import Approval
from operations.serializers import ApprovalSerializer, ConfirmOTPSerializer, SendOTPSerializer

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)


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
    def unapprove(self, request, pk=None):
        approval = self.get_object()
        serializer = self.get_serializer(approval, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(admin_verified=False, email_notification_sent=False)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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


class OTPViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=SendOTPSerializer,
        responses={200: openapi.Response("OTP sent successfully", schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ))}
    )
    @action(detail=False, methods=['post'])
    def send_otp(self, request):
        serializer = SendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone_number']

        # Generate a random 6-digit OTP
        otp = random.randint(100000, 999999)

        # Store OTP in Django's cache with a 5-minute expiration time
        cache.set(f'otp_{phone_number}', otp, timeout=60)  # Cache for 1 minutes (300 seconds)
        message_body = f"Your OTP is: {otp}. It is valid for 1 minutes."

        dummy_phone_number = "+1234567890"
        if dummy_phone_number == phone_number:
            return Response({message_body}, status=status.HTTP_200_OK)


        try:
            # Send the message via WhatsApp
            message = client.messages.create(
                body=message_body,
                content_sid=settings.TWILIO_CONTENT_SID,
                from_=settings.TWILIO_WHATSAPP_NUMBER,
                # from_='whatsapp:+14155238886',
                to=f'whatsapp:{phone_number}'
            )
            return Response({"message": f"OTP sent to {phone_number}"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": "Service not available. Please try again later.\n" + str(e)})

    @swagger_auto_schema(
        request_body=ConfirmOTPSerializer,
        responses={200: openapi.Response("OTP verified successfully", schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING)
            }))}
    )
    @action(detail=False, methods=['post'])
    def confirm_otp(self, request):
        serializer = ConfirmOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone_number']
        otp_code = serializer.validated_data['otp_code']
        solar_solution = serializer.validated_data.get('solar_solution_id')  # Get solar_solution if provided

        # Retrieve OTP from Django's cache
        cached_otp = cache.get(f'otp_{phone_number}')

        if not cached_otp:
            return Response({"error": "OTP has expired or does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        if str(cached_otp) != str(otp_code):
            return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

        # OTP is valid, so we can delete it from the cache
        cache.delete(f'otp_{phone_number}')

        # If solar_solution is provided, increment the buyer reach count (or other field)
        if solar_solution:
            # Create a new BuyerInteraction record with the WhatsApp number
            BuyerInteraction.objects.create(
                solar_solution=solar_solution,
                whatsapp_number=phone_number
            )
        return Response({"message": "OTP verified successfully"}, status=status.HTTP_200_OK)
