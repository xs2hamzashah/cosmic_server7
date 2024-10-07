from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ApprovalViewSet

# Create a router and register the ApprovalViewSet
router = DefaultRouter()
router.register(r'approvals', ApprovalViewSet, basename='approval')
#
urlpatterns = [
    # Include the router URLs
    path('', include(router.urls)),
]
