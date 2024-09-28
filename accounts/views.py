from rest_framework import viewsets
from .models import UserProfile
from .permissions import IsAdmin
from .serializers import UserProfileSerializer
from rest_framework.permissions import IsAuthenticated


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
