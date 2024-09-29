import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

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


