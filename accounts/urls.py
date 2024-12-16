# accounts/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, CompanyNamesListView

router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Include the router URLs here
    path('api/company-names/', CompanyNamesListView.as_view(), name='company-names'),
]
