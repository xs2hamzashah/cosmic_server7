from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ApprovalViewSet, OTPViewSet

# Create a router and register the ApprovalViewSet
router = DefaultRouter()
router.register(r'approvals', ApprovalViewSet, basename='approval')
router.register(r'otp', OTPViewSet, basename='otp')

#
urlpatterns = [
    # Include the router URLs
    path('', include(router.urls)),
]
