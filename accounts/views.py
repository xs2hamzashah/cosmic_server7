import django_filters
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.urls import reverse
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from cosmic_server7 import settings
from .models import UserProfile
from .permissions import IsAdmin
from .serializers import UserProfileSerializer, ForgotPasswordSerializer, PasswordResetSerializer, \
    CustomTokenObtainPairSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.select_related('user')
    serializer_class = UserProfileSerializer

    # Default serializer for user profile
    def get_serializer_class(self):
        if self.action == 'forgot_password':
            return ForgotPasswordSerializer
        elif self.action == 'reset_password':
            return PasswordResetSerializer
        return UserProfileSerializer

    class UserProfileFilter(django_filters.FilterSet):
        class Meta:
            model = UserProfile
            fields = ['role']

    filter_backends = [DjangoFilterBackend]
    filterset_class = UserProfileFilter  # Use the custom filter class

    def get_permissions(self):
        if self.action in ['create']:
            return [AllowAny()]
        elif self.action in ['update', 'partial_update', 'retrieve']:
            return [IsAuthenticated()]
        elif self.action == 'my_profile':
            return [IsAuthenticated()]
        return [AllowAny()]

    def perform_update(self, serializer):
        """ Custom update logic here """
        # Handle the nested user fields separately
        user_data = serializer.validated_data.pop('user', None)  # Remove user data from validated_data
        if user_data:
            for attr, value in user_data.items():
                setattr(serializer.instance.user, attr, value)
            serializer.instance.user.save()

        # Perform the update for UserProfile itself
        serializer.save()  # Save the UserProfile instance
        return serializer.instance  # Return the updated instance

    def destroy(self, request, *args, **kwargs):
        # Get the UserProfile instance
        user_profile = self.get_object()

        # Get the related User instance
        user = user_profile.user

        # Delete the UserProfile and the related User
        self.perform_destroy(user_profile)
        user.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(operation_description="User profile detail", responses={200: UserProfileSerializer()})
    @action(detail=False, methods=['get'])
    def my_profile(self, request):
        try:
            user_profile = UserProfile.objects.select_related('user').get(user=request.user)
            serializer = self.get_serializer(user_profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({'detail': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'], serializer_class=ForgotPasswordSerializer)
    def forgot_password(self, request):
        User = get_user_model()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']

            # Check if user exists with that email
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"detail": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

            reset_url = f"{settings.FRONTEND_BASE_URL}reset-password/{user.userprofile_id}/"

            # Send an email with the reset link
            send_mail(
                subject='Reset your password',
                message=f'Please use the following link to reset your password: {reset_url}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=True,
            )

            return Response({"detail": "Email sent. Please check your inbox."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], serializer_class=PasswordResetSerializer)
    def reset_password(self, request, pk=None):
        user_profile = self.get_object()  # Get the user object using the primary key (user ID) from the URL
        user = user_profile.user
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            new_password = serializer.validated_data['new_password']
            user.set_password(new_password)  # Use set_password to hash the password
            user.save()

            return Response({'detail': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
