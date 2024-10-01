from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SolarSolutionViewSet


# Create a router and register the viewset
router = DefaultRouter()
router.register(r'solar-solutions', SolarSolutionViewSet, basename='solar-solution')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
]
