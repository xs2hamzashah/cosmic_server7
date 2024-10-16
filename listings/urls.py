from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SolarSolutionViewSet, AnalyticsViewSet, TagListView

# Create a router and register the viewset
router = DefaultRouter()
router.register(r'solar-solutions', SolarSolutionViewSet, basename='solar-solution')
router.register(r'analytics', AnalyticsViewSet, basename='analytics')



# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
    path('tags/', TagListView.as_view(), name='tag-list'),
]
