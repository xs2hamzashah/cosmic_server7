from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SolarSolutionViewSet, AnalyticsViewSet, TagAPIView, ComponentAPIView

# Create a router and register the viewset
router = DefaultRouter()
router.register(r'solar-solutions', SolarSolutionViewSet, basename='solar-solution')
router.register(r'analytics', AnalyticsViewSet, basename='analytics')



# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
    path('tags/', TagAPIView.as_view(), name='tag-list-create'),
    path('components/', ComponentAPIView.as_view(), name='component-list-create'),

]
