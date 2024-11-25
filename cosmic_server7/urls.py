from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from cosmic_server7 import settings

schema_view = get_schema_view(
    openapi.Info(
        title="7Cosmic_Server",
        default_version='v1',
        description="",
        terms_of_service="",
        contact=openapi.Contact(email=""),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('api/auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('api/auth/refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/verify-token/', TokenVerifyView.as_view(), name='token_verify'),

    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/listings/', include('listings.urls')),
    path('api/operations/', include('operations.urls')),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # path('silk/', include('silk.urls', namespace='silk')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
