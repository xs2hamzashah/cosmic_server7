from django.shortcuts import render
from rest_framework import viewsets

from accounts.permissions import IsAdminOrSeller
from pricelist.models import Panel
from pricelist.serializers import PanelSerializer


# Create your views here.

class PanelViewSet(viewsets.ModelViewSet):
    queryset = Panel.objects.all()
    serializer_class = PanelSerializer
    permission_classes = [IsAdminOrSeller]

    def get_queryset(self):
        # If not an admin, return only panels for the current seller
        if not self.request.user.is_staff:
            return Panel.objects.filter(seller=self.request.user.userprofile)
        return Panel.objects.all()

    def perform_create(self, serializer):
        # Automatically set the seller to the current user's seller
        serializer.save(seller=self.request.user.userprofile)

    def perform_update(self, serializer):
        # Automatically set the seller to the current user's seller
        serializer.save(seller=self.request.user.userprofile)
