from django.urls import path, include
from rest_framework.routers import DefaultRouter

from pricelist.views import PanelViewSet


# Create a router and register the viewset
router = DefaultRouter()
router.register(r'panel', PanelViewSet, basename='panel')


# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
]
