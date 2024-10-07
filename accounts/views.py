import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import UserProfile
from .serializers import UserProfileSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.select_related('user')
    serializer_class = UserProfileSerializer

    class UserProfileFilter(django_filters.FilterSet):
        class Meta:
            model = UserProfile
            fields = ['role']

    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserProfileFilter  # Use the custom filter class

    def destroy(self, request, *args, **kwargs):
        # Get the UserProfile instance
        user_profile = self.get_object()

        # Get the related User instance
        user = user_profile.user

        # Delete the UserProfile and the related User
        self.perform_destroy(user_profile)
        user.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)